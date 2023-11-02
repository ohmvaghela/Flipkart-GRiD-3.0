#include <ros/ros.h>
#include <std_msgs/Float32MultiArray.h>
#include <vector>
#include <queue>

class PathPlanner
{
public:
    PathPlanner()
    {
        costmap_sub = nh.subscribe("costmap_topic", 1, &PathPlanner::updateCostmap, this);
        goal_sub = nh.subscribe("bot_goal_topic", 1, &PathPlanner::updateGoal, this);
        bot_sub = nh.subscribe("bot_loc_topic", 1, &PathPlanner::updateBot, this);
        path_pub = nh.advertise<std_msgs::Float32MultiArray>("path_topic", 10);
    }

    void updateCostmap(const std_msgs::Float32MultiArray::ConstPtr &data)
    {
        costmap = data->data;
    }

    void updateGoal(const std_msgs::Float32MultiArray::ConstPtr &data)
    {
        goal = data->data;
    }

    void updateBot(const std_msgs::Float32MultiArray::ConstPtr &data)
    {
        bot = data->data;
    }

    void pathPlanning(float botID)
    {
        for (auto &i : goal)
        {
            if (i[0] != botID)
            {
                costmap[i[1]][i[2]] = 1;
            }
        }

        std::vector<float> curLoc = getLoc(botID);
        std::vector<float> tarLoc = getLoc(botID);
        std_msgs::Float32MultiArray path = dijkstra(curLoc, tarLoc);
        path.push_front(botID);
        path_pub.publish(path);
    }

    void publishPath()
    {
        for (auto &i : bot)
        {
            pathPlanning(i[0]);
        }
    }

    std::vector<float> getLoc(float botID)
    {
        for (auto &item : bot)
        {
            if (item[0] == botID)
            {
                float x = item[1];
                float y = item[2];
                std::vector<float> curLoc = {x, y};
                return curLoc;
            }
        }
        return {};
    }

    std_msgs::Float32MultiArray dijkstra(const std::vector<float> &curLoc, const std::vector<float> &tarLoc)
    {
        int rows = costmap.size();
        int cols = costmap[0].size();
        std::vector<std::vector<float>> distances(rows, std::vector<float>(cols, std::numeric_limits<float>::infinity()));
        distances[curLoc[0]][curLoc[1]] = 0;
        std::vector<std::vector<std::pair<int, int>>> prev(rows, std::vector<std::pair<int, int>>(cols, {-1, -1}));
        std::priority_queue<std::pair<float, std::pair<int, int>>, std::vector<std::pair<float, std::pair<int, int>>>> pq;
        pq.push({0, {curLoc[0], curLoc[1]}});

        while (!pq.empty())
        {
            float dist = pq.top().first;
            int x = pq.top().second.first;
            int y = pq.top().second.second;
            pq.pop();
            if (x == tarLoc[0] && y == tarLoc[1])
            {
                break;
            }
            if (dist > distances[x][y])
            {
                continue;
            }

            std::vector<std::pair<int, int>> neighbors = getNeighbors(x, y, costmap);
            for (const auto &neighbor : neighbors)
            {
                int nx = neighbor.first;
                int ny = neighbor.second;
                float newDist = dist + 1; // Assuming each step has a distance of 1
                if (newDist < distances[nx][ny])
                {
                    distances[nx][ny] = newDist;
                    prev[nx][ny] = {x, y};
                    pq.push({newDist, {nx, ny}});
                }
            }
        }

        std::vector<float> path;
        int currX = tarLoc[0];
        int currY = tarLoc[1];
        while (currX != -1 && currY != -1)
        {
            path.push_back( currX);
            path.push_back( currY);
            int prevX = prev[currX][currY].first;
            int prevY = prev[currX][currY].second;
            currX = prevX;
            currY = prevY;
        }

        std_msgs::Float32MultiArray pathMsg;
        pathMsg.data = path;
        return pathMsg;
    }

    std::vector<std::vector<float>> getNeighbors(float x, float y)
    {
        int rows = costmap.size();
        int cols = costmap[0].size();
        std::vector<std::vector<float>> neighbors;

        if (x > 0 && costmap[static_cast<int>(x) - 1][static_cast<int>(y)] == 0)
        {
            neighbors.push_back({x - 1, y});
        }
        if (x < rows - 1 && costmap[static_cast<int>(x) + 1][static_cast<int>(y)] == 0)
        {
            neighbors.push_back({x + 1, y});
        }
        if (y > 0 && costmap[static_cast<int>(x)][static_cast<int>(y) - 1] == 0)
        {
            neighbors.push_back({x, y - 1});
        }
        if (y < cols - 1 && costmap[static_cast<int>(x)][static_cast<int>(y) + 1] == 0)
        {
            neighbors.push_back({x, y + 1});
        }

        return neighbors;
    }

private:
    ros::NodeHandle nh;
    ros::Subscriber costmap_sub;
    ros::Subscriber goal_sub;
    ros::Subscriber bot_sub;
    ros::Publisher path_pub;
    std::vector<float> costmap;
    std::vector<float> goal;
    std::vector<float> bot;
    int costmap_width = 14;  // Adjust these values according to your data
    int costmap_height = 14; // Adjust these values according to your data
};

int main(int argc, char **argv)
{
    ros::init(argc, argv, "path_planner");
    PathPlanner pathPlanner;
    pathPlanner.publishPath();
    ros::spin();
    return 0;
}
