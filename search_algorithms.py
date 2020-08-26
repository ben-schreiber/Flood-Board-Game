from data_structures import *
from heuristics import Heuristics


def search_helper(problem, data_struct):
    visited = dict()
    data_struct.push(problem.get_start_state())
    visited[problem.get_start_state()] = None, None
    while not data_struct.is_empty():
        temp = data_struct.pop()
        if problem.is_goal_state(temp):
            actions = []
            curr = temp
            while visited[curr][0] is not None:
                actions.insert(0, visited[curr][1])
                curr = visited[curr][0]
            return actions
        else:
            for successor in problem.get_successors(temp):
                if successor[0] not in visited:
                    data_struct.push(successor[0])
                    visited[successor[0]] = temp, successor[1]  # Key=State, Value=(PrevState, Action)


def depth_first_search(problem):
    """
    Search the deepest nodes in the search tree first.
    """
    return search_helper(problem, Stack())


def breadth_first_search(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    return search_helper(problem, Queue())


def uniform_cost_search(problem):
    """
    Search the node of least total cost first.
    """
    return a_star_search(problem, null=True)


def a_star_search(problem, null=False):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    visited = {str(problem.get_start_state()): (None, None)}
    p_queue = PriorityQueue()
    p_queue.push((problem.get_start_state(), 0), 0)
    while not p_queue.is_empty():
        temp_state, total_cost = p_queue.pop()
        if problem.is_goal_state(temp_state):
            actions = []
            curr = str(temp_state)
            while visited[curr][0] is not None:
                actions.insert(0, visited[curr][1])
                curr = str(visited[curr][0])
            return actions
        else:
            for successor in problem.get_successors(temp_state):
                str_state = str(successor[0])
                if str_state not in visited:
                    heuristic_obj = Heuristics(successor[0])
                    visited[str_state] = temp_state, successor[1]
                    new_total_cost = total_cost + successor[2]
                    p_queue.push((successor[0], new_total_cost), new_total_cost + heuristic_obj.get_weighted_sum(null=null))


def run_search_algorithm(algo_name, problem, heuristic=False):
    if algo_name == 'bfs':
        return breadth_first_search(problem)
    elif algo_name == 'dfs':
        return depth_first_search(problem)
    elif algo_name == 'ucs':
        return uniform_cost_search(problem)
    elif algo_name == 'astar':
        return a_star_search(problem, heuristic)
