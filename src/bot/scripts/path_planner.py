import rospy
from std_msgs.msg import Float32MultiArray
import heapq

class path_planner:
    def __init__(self):
        # 14x14 matrix
        self.costmap = Float32MultiArray() 

        # nx3 matrix [[botID,x,y],[botID,x,y],[botID,x,y]...]
        self.goal = Float32MultiArray() 

        # matrix [[botID,x1,y1,x2,y2,...],[botID,x1,y1,x2,y2,...],...]
        self.path = Float32MultiArray() 

        # nx3 matrix [[botID,x,y],[botID,x,y],[botID,x,y]...]
        self.bot = Float32MultiArray() 

        self.path_publisher = rospy.Publisher('path_topic', Float32MultiArray, queue_size=10)

        rospy.Subscriber('costmap_topic', Float32MultiArray, self.update_costmap)
        rospy.Subscriber('bot_goal_topic', Float32MultiArray, self.update_goal)
        rospy.Subscriber('bot_loc_topic', Float32MultiArray, self.update_bot)


    def update_costmap(self,data):
        self.costmap = data.data
    
    def update_goal(self,data):
        self.goal = data.data

    def update_bot(self,data):
        self.bot = data.data

    def path_planning(self,botID):
        
        for i in self.goal:
            if i[0] != botID:
                self.costmap[i[1],i[2]] = 1
        
        cur_loc = self.get_loc(botID)
        tar_loc = self.get_loc(botID)
        path  = self.dijkstra(cur_loc, tar_loc)
        self.path_publisher.publish(path)

    def publish_path(self):
        for i in self.bot:
            self.path_planning(i[0])

    def get_loc(self, bot_id):
        for item in self.bot:
            if item[0] == bot_id:
                x, y = item[1], item[2]
                cur_loc = [x, y]
                return cur_loc

    def dijkstra(self, cur_loc, tar_loc):
        rows = len(self.costmap)
        cols = len(self.costmap[0])
        distances = [[float('inf')] * cols for _ in range(rows)]
        distances[cur_loc[0]][cur_loc[1]] = 0
        visited = set()
        prev = [[None] * cols for _ in range(rows)]
        pq = [(0, cur_loc)]

        while pq:
            dist, node = heapq.heappop(pq)
            if node == tar_loc:
                break
            if node in visited:
                continue
            visited.add(node)

            neighbors = self.get_neighbors(node[0], node[1])
            for neighbor in neighbors:
                if neighbor in visited:
                    continue
                new_dist = dist + 1  # Assuming each step has a distance of 1
                if new_dist < distances[neighbor[0]][neighbor[1]]:
                    distances[neighbor[0]][neighbor[1]] = new_dist
                    prev[neighbor[0]][neighbor[1]] = node
                    heapq.heappush(pq, (new_dist, neighbor))

        path = self.reconstruct_path(prev, tar_loc)
        return path
   
                
    
def main():
    rospy.init_node('path_planner', anonymous=True)
    pp = path_planner()
    pp.publish_path()

    # Spin to keep the node running
    rospy.spin(10)

if __name__ == '__main__':
    main()