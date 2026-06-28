---
title: "Graph For Beginners [Problems | Pattern | Sample Solutions] - Discuss"
source: "https://leetcode.com/discuss/post/655708/graph-for-beginners-problems-pattern-sam-06fb/"
author:
published:
created: 2026-04-06
description: "Graph Problems For PracticeSharing some topic wise good Graph problems and sample solutions to observe on how to approach.List: https://leetcode.com/lis"
tags:
  - "clippings"
---
Graph For Beginners \[Problems | Pattern | Sample Solutions\]

[Graph Theory](https://leetcode.com/discuss/topic/graph/) [Career](https://leetcode.com/discuss/topic/career/)

**Graph Problems For Practice**

Sharing some topic wise good Graph problems and sample solutions to observe on how to approach.

List: [https://leetcode.com/list/x1wy4de7](https://leetcode.com/list/x1wy4de7)

1. **Union Find:**
	Identify if problems talks about finding groups or components.
	[https://leetcode.com/problems/friend-circles/](https://leetcode.com/problems/friend-circles/)  
	[https://leetcode.com/problems/redundant-connection/](https://leetcode.com/problems/redundant-connection/)  
	[https://leetcode.com/problems/most-stones-removed-with-same-row-or-column/](https://leetcode.com/problems/most-stones-removed-with-same-row-or-column/)  
	[https://leetcode.com/problems/number-of-operations-to-make-network-connected/](https://leetcode.com/problems/number-of-operations-to-make-network-connected/)  
	[https://leetcode.com/problems/satisfiability-of-equality-equations/](https://leetcode.com/problems/satisfiability-of-equality-equations/)  
	[https://leetcode.com/problems/accounts-merge/](https://leetcode.com/problems/accounts-merge/)
	All the above problems can be solved by Union Find algorithm with minor tweaks.  
	Below is a standard template for union find problems.
	```cpp
	class Solution {
	     vector<int>parent;
	     int find(int x) {
	         return parent[x] == x ? x : find(parent[x]);
	     }
	 public:
	     vector<int> findRedundantConnection(vector<vector<int>>& edges) {
	         int n = edges.size();
	         parent.resize(n+1, 0);
	         for (int i = 0; i <= n; i++)
	             parent[i] = i;
	         vector<int>res(2, 0);
	         for (int i = 0; i < n; i++) {
	             int x = find(edges[i][0]);
	             int y = find(edges[i][1]);
	             if (x != y)
	                 parent[y] = x;
	             else {
	                 res[0] = edges[i][0];
	                 res[1] = edges[i][1];
	             }
	         }
	         return res;
	     }
	 };
	```
2. **Depth First Search**
	1. **Start DFS from nodes at boundary:**  
		[https://leetcode.com/problems/surrounded-regions/](https://leetcode.com/problems/surrounded-regions/)  
		[https://leetcode.com/problems/number-of-enclaves/](https://leetcode.com/problems/number-of-enclaves/)
		```cpp
		class Solution {
		     int rows, cols;
		     void dfs(vector<vector<int>>& A, int i, int j) {
		         if (i < 0 || j < 0 || i >= rows || j >= cols)
		             return;
		         if (A[i][j] != 1) 
		             return;
		         A[i][j] = -1;
		         dfs(A, i+1, j);
		         dfs(A, i-1, j);
		         dfs(A, i, j+1);
		         dfs(A, i, j-1);
		     }
		 public:
		     int numEnclaves(vector<vector<int>>& A) {
		         if (A.empty()) return 0;
		         rows = A.size();
		         cols = A[0].size();
		         for (int i = 0; i < rows; i++) {
		             for (int j = 0; j < cols; j++) {
		                 if (i == 0 || j == 0 || i == rows-1 || j == cols-1)
		                     dfs(A, i, j);
		             }
		         }
		         int ans = 0;
		         for (int i = 0; i < rows; i++) {
		             for (int j = 0; j < cols; j++) {
		                 if (A[i][j] == 1)
		                     ans++;
		             }
		         }
		         return ans;
		     }
		 };
		```
		2. **Time taken to reach all nodes or share information to all graph nodes:**  
		[https://leetcode.com/problems/time-needed-to-inform-all-employees/](https://leetcode.com/problems/time-needed-to-inform-all-employees/)
		```cpp
		class Solution {
		     void dfs(unordered_map<int, vector<int>>&hm, int i, vector<int>& informTime, int &res, int curr) {
		         curr += informTime[i];
		         res = max(res, curr);
		         for (auto it = hm[i].begin(); it != hm[i].end(); it++)
		             dfs(hm, *it, informTime, res, curr);
		     }
		 public:
		     int numOfMinutes(int n, int headID, vector<int>& manager, vector<int>& informTime) {
		         unordered_map<int, vector<int>>hm;
		         for (int i = 0; i < n; i++)
		             if (manager[i] != -1) hm[manager[i]].push_back(i);
		         int res = 0, curr = 0;
		         dfs(hm, headID, informTime, res, curr);
		         return res;
		     }
		 };
		```
		3. **DFS from each unvisited node/Island problems**  
		[https://leetcode.com/problems/number-of-closed-islands/](https://leetcode.com/problems/number-of-closed-islands/)  
		[https://leetcode.com/problems/number-of-islands/](https://leetcode.com/problems/number-of-islands/)  
		[https://leetcode.com/problems/keys-and-rooms/](https://leetcode.com/problems/keys-and-rooms/)  
		[https://leetcode.com/problems/max-area-of-island/](https://leetcode.com/problems/max-area-of-island/)  
		[https://leetcode.com/problems/flood-fill/](https://leetcode.com/problems/flood-fill/)
		```cpp
		class Solution {
		     void dfs(vector<vector<char>>& grid, vector<vector<bool>>& visited, int i, int j, int m, int n) {
		         if (i < 0 || i >= m || j < 0 || j >= n) return;
		         if (grid[i][j] == '0' || visited[i][j]) return;
		         visited[i][j] = true;
		         dfs(grid, visited, i+1, j, m, n);
		         dfs(grid, visited, i, j+1, m, n);
		         dfs(grid, visited, i-1, j, m, n);
		         dfs(grid, visited, i, j-1, m, n);
		     }
		     public:
		     int numIslands(vector<vector<char>>& grid) {
		         if (grid.empty()) return 0;
		         int m = grid.size();
		         int n = grid[0].size();
		         vector<vector<bool>>visited(m, vector<bool>(n, false));
		         int res = 0;
		         for (int i = 0; i < m; i++) {
		             for (int j = 0; j < n; j++) {
		                 if (grid[i][j] == '1' && !visited[i][j]) {
		                     dfs(grid, visited, i, j, m, n);
		                     res++;
		                 }
		             }
		         }
		         return res;
		     }
		     };
		```
		4. **Cycle Find:**  
		[https://leetcode.com/problems/find-eventual-safe-states/](https://leetcode.com/problems/find-eventual-safe-states/)
		```cpp
		class Solution {
		     bool dfs(vector<vector<int>>& graph, int v, vector<int>& dp) {
		         if (dp[v])
		             return dp[v] == 1;
		         dp[v] = -1;
		         for (auto it = graph[v].begin(); it != graph[v].end(); it++)
		             if (!dfs(graph, *it, dp))
		                 return false;
		         dp[v] = 1;
		         return true;
		     }
		 public:
		     vector<int> eventualSafeNodes(vector<vector<int>>& graph) {
		         int V = graph.size();
		         vector<int>res;
		         vector<int>dp(V, 0);
		         for (int i = 0; i < V; i++) {    
		             if (dfs(graph, i, dp))
		                 res.push_back(i);
		         }
		         return res;
		     }
		```
		};
3. **Breadth First Search**
	1. **Shortest Path:**  
		[https://leetcode.com/problems/01-matrix/](https://leetcode.com/problems/01-matrix/)  
		[https://leetcode.com/problems/as-far-from-land-as-possible/](https://leetcode.com/problems/as-far-from-land-as-possible/)  
		[https://leetcode.com/problems/rotting-oranges/](https://leetcode.com/problems/rotting-oranges/)  
		[https://leetcode.com/problems/shortest-path-in-binary-matrix/](https://leetcode.com/problems/shortest-path-in-binary-matrix/)
		Start BFS from nodes from which shortest path is asked for.  
		Below is the sample BFS approach to find the path.
		```cpp
		class Solution {
		    public:
		    vector<vector<int>> updateMatrix(vector<vector<int>>& matrix) {
		        if (matrix.empty()) return matrix;
		        int rows = matrix.size();
		        int cols = matrix[0].size();
		        queue<pair<int, int>>pq;
		        for (int i = 0; i < rows; i++) {
		            for (int j = 0; j < cols; j++) {
		                if (matrix[i][j] == 0) {
		                    pq.push({i-1, j}), pq.push({i+1, j}), pq.push({i, j-1}), pq.push({i, j+1}); 
		                }
		            }
		        }
		        vector<vector<bool>>visited(rows, vector<bool>(cols, false));
		        int steps = 0;
		        while (!pq.empty()) {
		            steps++;
		            int size = pq.size();
		            for (int i = 0; i < size; i++) {
		                auto front = pq.front();
		                int l = front.first;
		                int r = front.second;
		                pq.pop();
		                if (l >= 0 && r >= 0 && l < rows && r < cols && !visited[l][r] && matrix[l][r] == 1) {
		                    visited[l][r] = true;
		                    matrix[l][r] = steps;
		                    pq.push({l-1, r}), pq.push({l+1, r}), pq.push({l, r-1}), pq.push({l, r+1});
		                }
		            }
		        }
		        return matrix;
		    }
		};
		```
4. **Graph coloring/Bipartition**  
	[https://leetcode.com/problems/possible-bipartition/](https://leetcode.com/problems/possible-bipartition/)  
	[https://leetcode.com/problems/is-graph-bipartite/](https://leetcode.com/problems/is-graph-bipartite/)
	Problems asks to check if its possible to divide the graph nodes into 2 groups  
	Apply BFS for same. Below is a sample graph coloring approach.
	```cpp
	class Solution {
	     public:
	         bool isBipartite(vector<vector<int>>& graph) {
	             int n = graph.size();
	             vector<int>color(n, -1);
	             for (int i = 0; i < n; i++) {
	                 if (color[i] != -1) continue;
	                 color[i] = 1;
	                 queue<int>q;
	                 q.push(i);
	                 while (!q.empty()) {
	                     int t = q.front();
	                     q.pop();
	                     for (int j = 0; j < graph[t].size(); j++) {
	                         if (color[graph[t][j]] == -1) {
	                             color[graph[t][j]] = 1-color[t];
	                             q.push(graph[t][j]);
	                         } else if (color[graph[t][j]] == color[t]) {
	                             return false;
	                         }
	                     }
	                 }
	             }
	             return true;
	         }
	     };
	```
5. **Topological Sort:**  
	Check if its directed acyclic graph and we have to arrange the elements in an order in which we need to select the most independent node at first. Number of in-node 0
	[https://leetcode.com/problems/course-schedule/](https://leetcode.com/problems/course-schedule/)  
	[https://leetcode.com/problems/course-schedule-ii/](https://leetcode.com/problems/course-schedule-ii/)
	Below is sample approach. Find if cycle is present, if not apply topological sort.
	```cpp
	class Solution {
	     int V;
	     list<int>*adj;
	     
	     bool isCyclicUtil(int v, vector<bool>&visited, vector<bool>&recStack) {
	         
	         visited[v] = true;
	         recStack[v] = true;
	         
	         for (auto it = adj[v].begin(); it != adj[v].end(); it++) {
	             if (!visited[*it] && isCyclicUtil(*it, visited, recStack))
	                 return true;
	             else if (recStack[*it])
	                 return true;
	         }
	         
	         recStack[v] = false;
	         return false;
	     }
	     
	     bool isCyclic() {
	         vector<bool>visited(V, false);
	         vector<bool>recStack(V, false);
	         
	         for (int i = 0; i < V; i++) {
	             if (isCyclicUtil(i, visited, recStack))
	                 return true;
	         }
	         
	         return false;
	     }
	     
	     void topologicalSortUtil(int v, vector<bool>&visited, vector<int>& res) {
	         visited[v] = true;
	         
	         for (auto it = adj[v].begin(); it != adj[v].end(); it++)
	             if (!visited[*it])
	                 topologicalSortUtil(*it, visited, res);
	         
	         res.push_back(v);
	     }
	     
	     vector<int>topologicalSort(int v) {
	         vector<int>res;
	         
	         vector<bool>visited(V, false);
	         topologicalSortUtil(v, visited, res);
	         
	         for (int i = 0; i < V; i++) {
	             if (!visited[i])
	                 topologicalSortUtil(i, visited, res);
	         }
	         
	         return res;
	     }
	     
	     public:
	     vector<int> findOrder(int numCourses, vector<vector<int>>& prerequisites) {
	         V = numCourses;
	         adj = new list<int>[V];
	     
	         unordered_map<int, vector<int>>hm;
	         
	         for (int i = 0; i < prerequisites.size(); i++) {
	             adj[prerequisites[i][0]].push_back(prerequisites[i][1]);
	             hm[prerequisites[i][1]].push_back(prerequisites[i][0]);
	         }
	         
	         if (isCyclic()) return vector<int>();
	         
	         int i = 0;
	         for (i = 0; i < V; i++) {
	             if (hm.find(i) == hm.end())
	                 break;
	         }
	         
	         return topologicalSort(i);
	     }
	```
	};
6. **Find Shortest Path (Dijkstra's/Bellman Ford)**  
	[https://leetcode.com/problems/network-delay-time/](https://leetcode.com/problems/network-delay-time/)
	**Dijkstras and Bellman Ford:**
	```cpp
	class Solution {
	    public:
	        int networkDelayTime(vector<vector<int>>& times, int N, int K) {
	            
	            priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>>pq;
	            vector<int>dist(N+1, INT_MAX);
	            
	            pq.push(make_pair(0, K));
	            dist[K] = 0;
	            
	            unordered_map<int, vector<pair<int, int>>>hm;
	            for (int i = 0; i < times.size(); i++)
	                hm[times[i][0]].push_back(make_pair(times[i][1], times[i][2]));
	            
	            while (!pq.empty()) {
	                pair<int, int>p = pq.top();
	                pq.pop();
	                
	                int u = p.second;
	                for (auto it = hm[u].begin(); it != hm[u].end(); it++) {
	                    int v = it->first;
	                    int w = it->second;
	                    
	                    if (dist[v] > dist[u] + w) {
	                        dist[v] = dist[u] + w;
	                        pq.push(make_pair(dist[v], v));
	                    }
	                }
	            }
	            
	            int res = 0;
	            for (int i = 1; i <= N; i++)
	                res = max(res, dist[i]);
	            
	            return res == INT_MAX ? -1 : res;
	        }
	    };
	    
	    class Solution {
	    public:
	        int networkDelayTime(vector<vector<int>>& times, int N, int K) {
	            
	            int n = times.size();
	            if (!n) return 0;
	            
	            vector<int>dist(N+1, INT_MAX);
	            int res = 0;
	            
	            dist[K] = 0;
	            for (int i = 0; i < N; i++) {
	                for (int j = 0; j < n; j++) {
	                    int u = times[j][0];
	                    int v = times[j][1];
	                    int w = times[j][2];
	                    if (dist[u] != INT_MAX && dist[u] + w < dist[v])
	                        dist[v] = w + dist[u];
	                }
	            }
	            
	            for (int i = 1; i <= N; i++)
	                res = max(res, dist[i]);
	            return res == INT_MAX ? -1 : res;
	        }
	    }
	```

Complete List: Below are mostly list of problems (mostly medium level and may 1 or 2 easy) which are better to start practice with:  
(Updated on 14th June '20)

**Union Find:**

1. [https://leetcode.com/problems/friend-circles/](https://leetcode.com/problems/friend-circles/)
2. [https://leetcode.com/problems/redundant-connection/](https://leetcode.com/problems/redundant-connection/)
3. [https://leetcode.com/problems/most-stones-removed-with-same-row-or-column/](https://leetcode.com/problems/most-stones-removed-with-same-row-or-column/)
4. [https://leetcode.com/problems/number-of-operations-to-make-network-connected/](https://leetcode.com/problems/number-of-operations-to-make-network-connected/)
5. [https://leetcode.com/problems/satisfiability-of-equality-equations/](https://leetcode.com/problems/satisfiability-of-equality-equations/)
6. [https://leetcode.com/problems/accounts-merge/](https://leetcode.com/problems/accounts-merge/)
7. [https://leetcode.com/problems/connecting-cities-with-minimum-cost/](https://leetcode.com/problems/connecting-cities-with-minimum-cost/)

**DFS:**  
DFS from boundary:

1. [https://leetcode.com/problems/surrounded-regions/](https://leetcode.com/problems/surrounded-regions/)
2. [https://leetcode.com/problems/number-of-enclaves/](https://leetcode.com/problems/number-of-enclaves/)

Shortest time:

1. [https://leetcode.com/problems/time-needed-to-inform-all-employees/](https://leetcode.com/problems/time-needed-to-inform-all-employees/)

Islands Variants

1. [https://leetcode.com/problems/number-of-closed-islands/](https://leetcode.com/problems/number-of-closed-islands/)
2. [https://leetcode.com/problems/number-of-islands/](https://leetcode.com/problems/number-of-islands/)
3. [https://leetcode.com/problems/keys-and-rooms/](https://leetcode.com/problems/keys-and-rooms/)
4. [https://leetcode.com/problems/max-area-of-island/](https://leetcode.com/problems/max-area-of-island/)
5. [https://leetcode.com/problems/flood-fill/](https://leetcode.com/problems/flood-fill/)
6. [https://leetcode.com/problems/coloring-a-border/](https://leetcode.com/problems/coloring-a-border/)

Hash/DFS:

1. [https://leetcode.com/problems/employee-importance/](https://leetcode.com/problems/employee-importance/)
2. [https://leetcode.com/problems/find-the-town-judge/](https://leetcode.com/problems/find-the-town-judge/)

Cycle Find:

1. [https://leetcode.com/problems/find-eventual-safe-states/](https://leetcode.com/problems/find-eventual-safe-states/)

**BFS:**  
BFS for shortest path:

1. [https://leetcode.com/problems/01-matrix/](https://leetcode.com/problems/01-matrix/)
2. [https://leetcode.com/problems/as-far-from-land-as-possible/](https://leetcode.com/problems/as-far-from-land-as-possible/)
3. [https://leetcode.com/problems/rotting-oranges/](https://leetcode.com/problems/rotting-oranges/)
4. [https://leetcode.com/problems/shortest-path-in-binary-matrix/](https://leetcode.com/problems/shortest-path-in-binary-matrix/)

**Graph coloring:**

1. [https://leetcode.com/problems/possible-bipartition/](https://leetcode.com/problems/possible-bipartition/)
2. [https://leetcode.com/problems/is-graph-bipartite/](https://leetcode.com/problems/is-graph-bipartite/)

**Topological Sort:**

1. [https://leetcode.com/problems/course-schedule-ii/](https://leetcode.com/problems/course-schedule-ii/)

**Shortest Path:**

1. [https://leetcode.com/problems/network-delay-time/](https://leetcode.com/problems/network-delay-time/)
2. [https://leetcode.com/problems/find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance/](https://leetcode.com/problems/find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance/)
3. [https://leetcode.com/problems/cheapest-flights-within-k-stops/](https://leetcode.com/problems/cheapest-flights-within-k-stops/)

Please correct the approach/solution if you find anything wrong.

Similar POST  
DP: [https://leetcode.com/discuss/general-discussion/662866/Dynamic-Programming-for-Practice-Problems-Patterns-and-Sample-Solutions](https://leetcode.com/discuss/general-discussion/662866/Dynamic-Programming-for-Practice-Problems-Patterns-and-Sample-Solutions)  
Sliding Window: [https://leetcode.com/discuss/general-discussion/657507/Sliding-Window-for-Beginners-Problems-or-Template-or-Sample-Solutions](https://leetcode.com/discuss/general-discussion/657507/Sliding-Window-for-Beginners-Problems-or-Template-or-Sample-Solutions)

Comments (125)

Here is list of problems, you can clone it.  
[https://leetcode.com/list/x1vj23fh](https://leetcode.com/list/x1vj23fh)

217

Show 18 Replies

Reply

You know what they say...

Gotta grind to shine

139

Show 2 Replies

Reply

[Eddie Tseng](https://leetcode.com/u/eddietseng1129/)

May 30, 2020

Thanks! LeetCode should have a "save article" icon!!!

81

Show 2 Replies

Reply

From other comments and from this post - [https://leetcode.com/discuss/interview-question/753236/List-of-graph-algorithms-for-coding-interview](https://leetcode.com/discuss/interview-question/753236/List-of-graph-algorithms-for-coding-interview)

**Strongly Connected Components (SCC) / Finding Bridge and Articulation point**  
[https://leetcode.com/problems/critical-connections-in-a-network/](https://leetcode.com/problems/critical-connections-in-a-network/)

**Minimum Spanning Tree (MST) - Prim's and Kruskal's algos**  
[https://leetcode.com/problems/connecting-cities-with-minimum-cost/](https://leetcode.com/problems/connecting-cities-with-minimum-cost/)  
[https://leetcode.com/problems/optimize-water-distribution-in-a-village/](https://leetcode.com/problems/optimize-water-distribution-in-a-village/)

**Hierholzer's algorithm for Eulerian circuits.**  
[https://leetcode.com/problems/reconstruct-itinerary/](https://leetcode.com/problems/reconstruct-itinerary/)

**A Search**  
[https://leetcode.com/problems/sliding-puzzle/](https://leetcode.com/problems/sliding-puzzle/)

47

Show 1 Replies

Reply

[Prakash Kantheti](https://leetcode.com/u/specter03/)

May 28, 2020

Thanks for this! While we are on the topic, could people share similar Graph articles that you may have come across in leetcode (if there are any great ones out there)?

26

Show 1 Replies

Reply

[Jandos Iskakov](https://leetcode.com/u/jisqaqov/)

May 28, 2020

great, can you please make solutions collapsible, so people could solve it first not looking at solutions

25

Reply

[Jandos Iskakov](https://leetcode.com/u/jisqaqov/)

May 28, 2020

you did really good job, i would appreciate there could be such posts more,  
can you make also for advanced level

23

Show 3 Replies

Reply

Amazing. You can include tree problems too. Tree is a special type of graph.

8

Show 6 Replies

Reply

[Sabira Farheen](https://leetcode.com/u/sabira007x/)

May 29, 2020

[@wh0ami](https://leetcode.com/wh0ami) Can you kindly do the same for dynamic programming?

6

Show 5 Replies

Reply