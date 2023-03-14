from queue import Queue


class MaxFlow:
    def __init__(self, size):
        self.size = size
        self.residual = [[0 for i in range(size)] for j in range(size)]
        self.maxflowgraph = [[0 for i in range(size)] for j in range(size)]
        # 记录最大流图，初始都为0
        self.flow = [0 for i in range(size)]
        # 记录增广路径前进过程记录的最小流量
        self.pre = [float('inf') for i in range(size)]
        # 记录增广路径每个节点的前驱
        self.q = Queue()

    def init_residual(self, origins):
        '''
        o: start, end, capability
        '''
        for o in origins:
            self.residual[o[0]][o[1]] = o[2]

    def remove_inf(self):
        return [int(x) if x != float('inf') else -1 for x in self.pre]

    def deinit_residual(self):
        tuple = []
        for i in range(len(self.residual)):
            for j in range(len(self.residual)):
                if self.maxflowgraph[i][j] != 0:
                    tuple.append([i, j, self.residual[i][j]])
        return tuple

    def BFS(self, source, sink):
        self.q.empty()  # 清空队列

        for i in range(self.size):
            self.pre[i] = float('inf')

        self.flow[source] = float('inf')  # 这里要是不改，那么找到的路径的流量永远是0
        # 不用将flow的其他清零
        self.q.put(source)
        while (not self.q.empty()):
            index = self.q.get()
            if (index == sink):
                break
            for i in range(self.size):
                if ((i != source) & (self.residual[index][i] > 0) & (self.pre[i] == float('inf'))):
                    # i!=source，从source到source不用分析了
                    # residual[index][i]>0，边上有流量可以走
                    # pre[i]==float('inf')，代表BFS还没有延伸到这个点上
                    self.pre[i] = index
                    self.flow[i] = min(self.flow[index], self.residual[index][i])
                    self.q.put(i)
        if (self.pre[sink] == float('inf')):
            # 汇点的前驱还是初始值，说明已无增广路径
            return -1
        else:
            return self.flow[sink]

    def maxflow(self, source, sink):
        sumflow = 0  # 记录最大流，一直累加
        augmentflow = 0  # 当前寻找到的增广路径的最小通过流量
        residual_set = []
        while (True):
            augmentflow = self.BFS(source, sink)
            if (augmentflow == -1):
                break  # 返回-1说明已没有增广路径
            k = sink
            while (k != source):  # k回溯到起点，停止
                self.prev = self.pre[k]  # 走的方向是从prev到k
                self.maxflowgraph[self.prev][k] += augmentflow
                self.residual[self.prev][k] -= augmentflow  # 前进方向消耗掉了
                self.residual[k][self.prev] += augmentflow  # 反向边
                k = self.prev
            sumflow += augmentflow
            residual_set.append([self.flow[sink], self.remove_inf(), self.deinit_residual()])
            print("BFS:\n", self.flow[sink], self.pre)
            print("residual\n", self.residual)
        print("maxgraph\n", self.maxflowgraph)
        return sumflow, self.maxflowgraph, residual_set

    def transferToTuple(self):
        '''
        建议先判断sumflow是否为0，如果为0就是连不上
        '''
        tuple = []
        for i in range(len(self.maxflowgraph)):
            for j in range(len(self.maxflowgraph)):
                if self.maxflowgraph[i][j] != 0:
                    tuple.append([i, j, self.maxflowgraph[i][j]])
        return tuple

# origins = [
#     [0, 1, 3],
#     [0, 2, 2],
#     [1, 2, 1],
#     [1, 3, 3],
#     [1, 4, 4],
#     [2, 4, 2],
#     [3, 5, 2],
#     [4, 5, 3]
# ]
#
# max_flow = MaxFlow(6)
# max_flow.init_residual(origins)
# result, max_graph = max_flow.maxflow(0, 5)
# print(result)
# print(max_graph)  # 最大流图
# print(max_flow.transferToTuple())
