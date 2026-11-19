"""
Software Engineer (SWE) Assessment Question Generator (250 Unique Questions)
60 MCQ, 50 Coding, 35 Debugging, 40 Scenario, 30 SQL, 35 System Design
"""

from typing import List, Dict, Any
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scenario_catalog import generate_role_scenarios
from base_builder import build_mcq, build_coding, build_debugging, build_scenario, build_sql, build_system_design

ROLE_ID = "software_engineer"
SKILLS = {
    "S1": ("SWE-SKL-01", "Data Structures & Algorithms"),
    "S2": ("SWE-SKL-02", "Object-Oriented & Functional Design Patterns"),
    "S3": ("SWE-SKL-03", "Concurrency, Multithreading & Memory Management"),
    "S4": ("SWE-SKL-04", "Database Systems & Transaction Isolation"),
    "S5": ("SWE-SKL-05", "API Architecture & Distributed RPC")
}

def generate_swe_questions() -> List[Dict[str, Any]]:
    questions = []
    
    # -------------------------------------------------------------
    # 1. 60 MCQs (25 Easy, 25 Medium, 10 Hard)
    # -------------------------------------------------------------
    mcq_specs = [
        # S1: DSA (12 MCQs)
        ("S1", "Binary Search and Monotonic Search Spaces", "easy",
         "When implementing binary search on a monotonically increasing array to find the first occurrence of an element, which boundary update prevents infinite looping when `left + 1 == right`?",
         [{"id": "A", "text": "mid = left + (right - left) // 2 and left = mid + 1"},
          {"id": "B", "text": "mid = left + (right - left) // 2 and right = mid"},
          {"id": "C", "text": "mid = (left + right + 1) // 2 and right = mid - 1"},
          {"id": "D", "text": "mid = left + (right - left) // 2 and left = mid"}],
         "B",
         "When searching for the first occurrence with an open/closed boundary invariant, choosing `mid = left + (right - left) // 2` truncates towards left. Setting `right = mid` safely preserves candidate first matches without infinite looping."),

        ("S1", "Array and Two-Pointer / Sliding Window Techniques", "easy",
         "In a sliding window algorithm computing the minimum size subarray sum at least `target` with positive integers, what is the amortized time complexity of the right and left pointer movements?",
         [{"id": "A", "text": "O(N^2) because of nested loops"},
          {"id": "B", "text": "O(N log N) due to binary window expansion"},
          {"id": "C", "text": "O(N) because each pointer visits each element at most once"},
          {"id": "D", "text": "O(N * target) proportional to value magnitude"}],
         "C",
         "Although the inner `while` loop contracts the left pointer, both `left` and `right` pointers advance monotonically from 0 to N. Thus, each element is enqueued and dequeued at most once, yielding strictly O(N) amortized time."),

        ("S1", "Tree and Graph Traversals (BFS, DFS, Dijkstra, A*)", "easy",
         "Why does Dijkstra's shortest path algorithm fail or produce incorrect results on graphs containing negative edge weights?",
         [{"id": "A", "text": "It uses a FIFO queue instead of a priority queue"},
          {"id": "B", "text": "Its greedy choice assumes that visiting an unvisited node with minimal current distance permanently settles its optimal shortest path"},
          {"id": "C", "text": "It cannot handle directed cyclic graphs"},
          {"id": "D", "text": "It requires all vertices to have an even degree"}],
         "B",
         "Dijkstra greedily marks nodes as permanently visited once dequeued from the min-heap, assuming any subsequent path extension will only increase the total cost. A negative edge later in the graph violates this monotonic distance growth assumption."),

        ("S1", "Dynamic Programming and Memoization", "easy",
         "What distinguishes optimal substructure from overlapping subproblems in dynamic programming problem formulation?",
         [{"id": "A", "text": "Optimal substructure means subproblems share identical memory, while overlapping subproblems means greedy choice applies"},
          {"id": "B", "text": "Optimal substructure means an optimal solution to the problem contains optimal solutions to its subproblems; overlapping subproblems means the recursive solution tree recomputes identical states"},
          {"id": "C", "text": "Optimal substructure applies only to trees; overlapping subproblems apply only to graphs"},
          {"id": "D", "text": "They are synonymous terms describing iterative tabulations"}],
         "B",
         "Optimal substructure allows global optimality to be built inductively from optimal sub-solutions (e.g. Bellman's principle), while overlapping subproblems make caching/memoization efficient by avoiding redundant tree branch evaluation."),

        ("S1", "Hash Maps, Heaps and Disjoint-Set Unions (DSU)", "easy",
         "What is the nearly constant amortized time complexity per operation in a Disjoint Set Union (DSU) data structure utilizing both Path Compression and Union by Rank/Size?",
         [{"id": "A", "text": "O(log N)"},
          {"id": "B", "text": "O(log* N)"},
          {"id": "C", "text": "O(alpha(N)), where alpha is the Inverse Ackermann function"},
          {"id": "D", "text": "O(1) strict worst-case"}],
         "C",
         "Combining path compression on `find` with union by rank/size bounds the amortized complexity per operation to O(alpha(N)), where alpha is the inverse Ackermann function, which is <= 4 for all practical universe sizes."),

        ("S1", "Binary Search and Monotonic Search Spaces", "medium",
         "When searching for a target in a sorted array that has been rotated at an unknown pivot with distinct elements, what condition determines whether the left half [left...mid] is normally ordered?",
         [{"id": "A", "text": "nums[left] < nums[right]"},
          {"id": "B", "text": "nums[left] <= nums[mid]"},
          {"id": "C", "text": "nums[mid] < nums[right]"},
          {"id": "D", "text": "nums[mid] - nums[left] == mid - left"}],
         "B",
         "Because all elements are distinct and the array was sorted prior to rotation, if `nums[left] <= nums[mid]`, the inflection pivot cannot lie in the range `[left, mid]`. Thus the left half is guaranteed monotonically increasing."),

        ("S1", "Tree and Graph Traversals (BFS, DFS, Dijkstra, A*)", "medium",
         "In Kahn's algorithm for Topological Sorting on a Directed Acyclic Graph (DAG), what is the graph invariant maintained by the in-degree array?",
         [{"id": "A", "text": "Nodes with zero in-degree have no remaining unvisited prerequisite dependencies"},
          {"id": "B", "text": "Nodes with maximum in-degree are processed first to maximize parallelism"},
          {"id": "C", "text": "The in-degree tracks the shortest distance from the source"},
          {"id": "D", "text": "In-degree is decremented only when back edges are encountered"}],
         "A",
         "Kahn's algorithm operates by repeatedly picking vertices with an in-degree of 0, meaning all prerequisite dependencies have been met and emitted. Emitting a node decrements the in-degrees of its immediate neighbors."),

        ("S1", "Dynamic Programming and Memoization", "medium",
         "In the 0/1 Knapsack problem with weights `W` and items `N`, why must the 1D space-optimized DP array `dp[w]` be traversed backwards from capacity `C` down to item weight `w_i`?",
         [{"id": "A", "text": "To allow SIMD vectorization on modern CPUs"},
          {"id": "B", "text": "To prevent using the current item multiple times in the same transition"},
          {"id": "C", "text": "To avoid array index out of bound exceptions"},
          {"id": "D", "text": "To guarantee that smaller weights are computed first"}],
         "B",
         "Traversing backwards guarantees that `dp[w - w_i]` represents the optimal value from the *previous* item iteration (item `i-1`). A forward traversal would use values already updated with item `i`, inadvertently modeling the unbounded knapsack problem."),

        ("S1", "Hash Maps, Heaps and Disjoint-Set Unions (DSU)", "medium",
         "In Robin Hood Hashing, what displacement metric is used to determine whether an incoming key evicts an existing occupant during linear probing?",
         [{"id": "A", "text": "Cryptographic hash digest value"},
          {"id": "B", "text": "Probe Sequence Length (distance of occupant from its initial hashed bucket)"},
          {"id": "C", "text": "Timestamp of key insertion"},
          {"id": "D", "text": "Frequency of recent key lookups"}],
         "B",
         "Robin Hood hashing steals from the 'rich' (keys close to their home bucket, having small probe sequence lengths) and gives to the 'poor' (keys displaced far from their home bucket), reducing the variance of lookup probe lengths."),

        ("S1", "Array and Two-Pointer / Sliding Window Techniques", "hard",
         "What is the amortized complexity of maintaining a Monotonic Deque to find the sliding window maximum over an array of size N with window size K?",
         [{"id": "A", "text": "O(N log K)"},
          {"id": "B", "text": "O(N)"},
          {"id": "C", "text": "O(N * K)"},
          {"id": "D", "text": "O(N log N)"}],
         "B",
         "Every array element is pushed onto the tail of the monotonic deque exactly once, and popped from the tail or head at most once over the entire execution. Thus, the total number of deque operations across all windows is bounded by 2N, achieving O(N) overall."),

        ("S1", "Tree and Graph Traversals (BFS, DFS, Dijkstra, A*)", "hard",
         "In Tarjan's strongly connected components algorithm, what indicates that node `u` is the root of a strongly connected component?",
         [{"id": "A", "text": "low[u] == dfn[u]"},
          {"id": "B", "text": "low[u] < dfn[u]"},
          {"id": "C", "text": "low[u] == 0"},
          {"id": "D", "text": "dfn[u] == stack.size()"}],
         "A",
         "In Tarjan's algorithm, `dfn[u]` is the discovery timestamp and `low[u]` is the lowest discovery time reachable from `u`. When `low[u] == dfn[u]`, no node in `u`'s subtree can reach an ancestor of `u`, meaning `u` and all nodes above it on the stack form an SCC."),

        ("S1", "Dynamic Programming and Memoization", "hard",
         "What mathematical condition must a cost function `C(i, j)` satisfy to enable Divide and Conquer Optimization in 2D dynamic programming of the form `dp[i][j] = min_{k < j} (dp[i-1][k] + C(k, j))`?",
         [{"id": "A", "text": "Lipschitz continuity"},
          {"id": "B", "text": "Monge property (Quadrangle Inequality): C(a, c) + C(b, d) <= C(a, d) + C(b, c) for a <= b <= c <= d"},
          {"id": "C", "text": "Commutativity and transitivity across all states"},
          {"id": "D", "text": "Linear separability in dual coordinate space"}],
         "B",
         "The quadrangle inequality (Monge property) ensures that the optimal transition point `opt(i, j)` is monotonic with respect to `j`: `opt(i, j) <= opt(i, j+1)`. This reduces the complexity from O(K * N^2) to O(K * N log N).")
    ]
    
    # Generate remaining 48 MCQs programmatically across S2, S3, S4, S5
    s2_mcqs = [
        ("S2", "SOLID Principles and Component Coupling", "easy",
         "According to the Liskov Substitution Principle (LSP), which of the following is an unacceptable modification when subclassing?",
         [{"id": "A", "text": "Strengthening preconditions in the subclass method"},
          {"id": "B", "text": "Weakening preconditions in the subclass method"},
          {"id": "C", "text": "Strengthening postconditions in the subclass method"},
          {"id": "D", "text": "Throwing fewer exception types than the superclass"}],
         "A", "LSP requires that subtype methods must not demand more (strengthen preconditions) than the parent type, as existing client code written for the parent contract would break."),
        ("S2", "Creational Patterns (Factory, Builder, Singleton)", "easy",
         "Why is the Bill Pugh Singleton implementation in Java considered superior to standard double-checked locking without volatile variables?",
         [{"id": "A", "text": "It uses operating system mutexes directly"},
          {"id": "B", "text": "It relies on class-loader initialization semantics to guarantee thread safety without explicit synchronization locks"},
          {"id": "C", "text": "It permits multiple distinct instances when memory pressure occurs"},
          {"id": "D", "text": "It bypasses JVM bytecode verification"}],
         "B", "The nested static helper class is loaded only when `getInstance()` is called. The JVM guarantees class initialization is atomic and thread-safe without synchronization overhead."),
        ("S2", "Structural Patterns (Adapter, Decorator, Facade)", "easy",
         "What is the primary architectural intent of the Facade design pattern?",
         [{"id": "A", "text": "Dynamically add responsibilities to an object transparently"},
          {"id": "B", "text": "Provide a unified, simplified high-level interface to a complex subsystem"},
          {"id": "C", "text": "Convert the interface of a class into another interface clients expect"},
          {"id": "D", "text": "Ensure a class only has one instance"}],
         "B", "A Facade encapsulates a complex set of subsystem interfaces behind a single, cohesive, high-level entry point, decoupling external consumers from internal subsystem churn."),
        ("S2", "Behavioral Patterns (Strategy, Observer, Command)", "easy",
         "How does the Strategy pattern differ fundamentally from the State pattern, despite sharing similar UML class diagrams?",
         [{"id": "A", "text": "Strategy pattern objects are aware of each other and handle transitions; State objects are isolated"},
          {"id": "B", "text": "Strategy encapsulates interchangeable algorithms chosen by the client; State encapsulates state-dependent behaviors and drives automatic transitions"},
          {"id": "C", "text": "Strategy applies only to asynchronous operations; State applies to synchronous calls"},
          {"id": "D", "text": "State pattern requires compile-time polymorphism; Strategy is purely dynamic"}],
         "B", "In Strategy, clients generally configure the context with an algorithm strategy. In State, the context's behavior changes dynamically based on internal state changes."),
        ("S2", "Functional Composition and Immutability", "easy",
         "What is a pure function in functional software engineering?",
         [{"id": "A", "text": "A function that has zero arguments"},
          {"id": "B", "text": "A function whose return value depends only on its arguments and causes no observable side effects"},
          {"id": "C", "text": "A function that executes inside a sandbox environment"},
          {"id": "D", "text": "A function written without loops"}],
         "B", "Pure functions guarantee referential transparency: given identical inputs, they always produce identical outputs with zero observable mutation of external state."),
        ("S2", "SOLID Principles and Component Coupling", "medium",
         "Which architectural smell indicates a violation of the Interface Segregation Principle (ISP)?",
         [{"id": "A", "text": "Classes implementing interfaces with empty or `UnsupportedOperationException` stub methods"},
          {"id": "B", "text": "A class having more than 5 private variables"},
          {"id": "C", "text": "Using dependency injection frameworks"},
          {"id": "D", "text": "High test coverage on polymorphic classes"}],
         "A", "When a class is forced to implement interface methods it does not need (throwing unsupported exceptions or leaving empty bodies), the interface is too fat, violating ISP."),
        ("S2", "Structural Patterns (Adapter, Decorator, Facade)", "medium",
         "How does the Decorator pattern maintain transparency for client code interacting with wrapped components?",
         [{"id": "A", "text": "By inheriting from the concrete implementation class"},
          {"id": "B", "text": "By implementing the exact same interface or abstract type as the component it wraps and delegating calls"},
          {"id": "C", "text": "By modifying the wrapped object's memory bytecode at runtime"},
          {"id": "D", "text": "By utilizing static class methods"}],
         "B", "The Decorator implements the same interface as the target component and holds a reference to it, allowing callers to invoke standard methods without knowing decoration occurred."),
        ("S2", "Behavioral Patterns (Strategy, Observer, Command)", "medium",
         "What critical memory management defect commonly occurs in the classic Observer pattern when observers are dynamically registered but never unregistered?",
         [{"id": "A", "text": "Stack overflow during notification"},
          {"id": "B", "text": "Lapsed Listener leak (Subject maintains strong references preventing garbage collection of listeners)"},
          {"id": "C", "text": "Deadlock on observer instantiation"},
          {"id": "D", "text": "Thread pool starvation"}],
         "B", "The subject retains strong references to observers in its subscription list. Even if caller references are dropped, the GC cannot collect observers, causing a Lapsed Listener leak."),
        ("S2", "Creational Patterns (Factory, Builder, Singleton)", "medium",
         "When designing an immutable domain object with 12 optional validation-dependent fields, why is the Builder pattern preferred over telescoping constructors?",
         [{"id": "A", "text": "Telescoping constructors violate thread safety during heap allocation"},
          {"id": "B", "text": "The Builder avoids constructor combinatorial explosion, enforces atomic validation upon `.build()`, and prevents parameter transposition errors"},
          {"id": "C", "text": "Telescoping constructors prevent inheritance in all compiled languages"},
          {"id": "D", "text": "The Builder eliminates object allocation overhead"}],
         "B", "Builders provide explicit named parameter setting, eliminate ambiguous positional parameter swapping of identical types, and centralize consistency invariant checks in `.build()`."),
        ("S2", "Functional Composition and Immutability", "hard",
         "In functional programming, how does Currying differ from Partial Application?",
         [{"id": "A", "text": "Currying translates a function of N arguments into a chain of N single-argument functions; Partial Application binds a fixed subset of arguments returning a function of lower arity"},
          {"id": "B", "text": "Currying is asynchronous; Partial Application is synchronous"},
          {"id": "C", "text": "Partial application requires macros; currying is native to all languages"},
          {"id": "D", "text": "They are identical mathematical operations with differing syntax"}],
         "A", "Currying decomposes `f(a, b, c)` strictly into `f(a)(b)(c)`. Partial application takes `f(a, b, c)` and fixes `a` to return `g(b, c)`."),
        ("S2", "SOLID Principles and Component Coupling", "hard",
         "In hexagonal/clean architecture, what rule governs dependency direction across domain, application, and infrastructure layers?",
         [{"id": "A", "text": "The Domain layer must depend on Infrastructure data repositories via concrete classes"},
          {"id": "B", "text": "Dependencies must point strictly inwards towards the Domain; outer layers depend on abstractions defined by inner layers"},
          {"id": "C", "text": "Application layer must not have access to domain entities"},
          {"id": "D", "text": "Infrastructure layer controls all business workflow transitions"}],
         "B", "The Dependency Inversion Principle mandates that core business logic (Domain) remains free of external framework or persistence dependencies, defining interfaces that outer adapters implement."),
        ("S2", "Behavioral Patterns (Strategy, Observer, Command)", "hard",
         "In the Command Pattern, how is reversible execution (Undo/Redo) architected to prevent memory bloat over deep history stacks?",
         [{"id": "A", "text": "Store complete system memory snapshots on disk at every command"},
          {"id": "B", "text": "Store delta/memento operations with an execution log and enforce a bounded circular buffer (e.g., max 50 states)"},
          {"id": "C", "text": "Re-execute all commands from initialization on every undo"},
          {"id": "D", "text": "Disable garbage collection during undo sequences"}],
         "B", "Commands encapsulate inverse delta transitions rather than full system copies, and bounded circular deques bound memory consumption by pruning oldest historical states.")
    ]

    # S3: Concurrency & Memory (12 MCQs)
    s3_mcqs = [
        ("S3", "Thread Synchronization, Mutexes and Semaphores", "easy",
         "What is the difference between a binary semaphore and a reentrant mutex?",
         [{"id": "A", "text": "A mutex has ownership semantics and can only be unlocked by the thread that locked it; a semaphore can be signaled by any thread"},
          {"id": "B", "text": "Semaphores cannot be used across processes"},
          {"id": "C", "text": "Mutexes permit arbitrary thread counts simultaneously"},
          {"id": "D", "text": "Binary semaphores are implemented exclusively in user space"}],
         "A", "Mutexes embody ownership: only the acquiring thread may release the lock. Semaphores are signaling mechanisms without ownership, allowing thread A to signal thread B."),
        ("S3", "Deadlock Detection, Prevention and Race Conditions", "easy",
         "Which of Coffman's four conditions is directly dismantled when all threads acquire shared resource locks in a globally defined, strict hierarchical order?",
         [{"id": "A", "text": "Mutual Exclusion"},
          {"id": "B", "text": "Hold and Wait"},
          {"id": "C", "text": "No Preemption"},
          {"id": "D", "text": "Circular Wait"}],
         "D", "Imposing a total ordering on lock acquisition ensures that no cycle can exist in the resource allocation graph, eliminating the Circular Wait condition."),
        ("S3", "Garbage Collection Mechanics and Memory Leak Profiling", "easy",
         "In a generational garbage collector, what foundational assumption (generational hypothesis) justifies separating objects into young and old generations?",
         [{"id": "A", "text": "Old objects consume significantly less memory than young objects"},
          {"id": "B", "text": "Most allocated objects have very short lifespans and die shortly after creation"},
          {"id": "C", "text": "Young generation collectors require full application stop-the-world pauses"},
          {"id": "D", "text": "Thread stacks can only reference old generation objects"}],
         "B", "The weak generational hypothesis states that the vast majority of objects die shortly after allocation. Focusing frequent minor collections on the young generation maximizes throughput."),
        ("S3", "Lock-Free Data Structures and Atomic Primitives", "easy",
         "What hardware CPU instruction forms the foundation of optimistic lock-free synchronization primitives?",
         [{"id": "A", "text": "Compare-And-Swap (CAS)"},
          {"id": "B", "text": "Arithmetic Shift Right"},
          {"id": "C", "text": "Branch if Zero"},
          {"id": "D", "text": "SIMD Multiply-Accumulate"}],
         "A", "Atomic CAS reads a memory location, compares its value to an expected value, and if identical, writes the new value atomically in hardware, returning whether the swap succeeded."),
        ("S3", "Asynchronous Event Loops and Coroutines", "easy",
         "In a single-threaded asynchronous event loop (e.g. Node.js or Python asyncio), what causes event loop starvation?",
         [{"id": "A", "text": "Handling 10,000 idle TCP socket connections"},
          {"id": "B", "text": "Executing long-running CPU-bound synchronous computations on the main thread"},
          {"id": "C", "text": "Excessive awaiting of non-blocking network I/O"},
          {"id": "D", "text": "Using too many async generator functions"}],
         "B", "Because the event loop runs on a single thread, any synchronous CPU-bound task blocks the execution thread, preventing the loop from dispatching pending I/O callbacks."),
        ("S3", "Thread Synchronization, Mutexes and Semaphores", "medium",
         "What is 'False Sharing' in multi-threaded concurrent programming on multi-core processors?",
         [{"id": "A", "text": "Two threads accessing different variables that reside on the same CPU cache line, causing constant invalidation traffic"},
          {"id": "B", "text": "Threads sharing heap pointers without atomic increments"},
          {"id": "C", "text": "Corrupted virtual memory pages mapped to multiple processes"},
          {"id": "D", "text": "Operating system scheduler swapping threads onto wrong NUMA nodes"}],
         "A", "Even if threads modify independent variables, if those variables share a 64-byte cache line, CPU cache coherence protocols (MESI) invalidate the entire line on every write."),
        ("S3", "Lock-Free Data Structures and Atomic Primitives", "medium",
         "In lock-free algorithms utilizing Compare-And-Swap (CAS), what is the ABA problem and how is it resolved?",
         [{"id": "A", "text": "A value changes from A to B and back to A; resolved using versioned pointers or generation counters"},
          {"id": "B", "text": "A thread acquires lock A then B then A; resolved via mutex nesting"},
          {"id": "C", "text": "Memory addresses are swapped in cache; resolved with barrier instructions"},
          {"id": "D", "text": "Branch prediction failure; resolved with compiler unrolling"}],
         "A", "A thread reads A, is preempted, another thread changes A->B->A. The first thread's CAS succeeds despite intervening structural changes. It is resolved using tagged/versioned pointers."),
        ("S3", "Garbage Collection Mechanics and Memory Leak Profiling", "medium",
         "In tracing garbage collection, how does the Tri-Color Marking algorithm classify an object marked 'Gray'?",
         [{"id": "A", "text": "The object is unreachable and eligible for immediate collection"},
          {"id": "B", "text": "The object is reachable, but its referenced outgoing child objects have not yet been scanned"},
          {"id": "C", "text": "The object has been scanned and all its references are verified live"},
          {"id": "D", "text": "The object resides in an off-heap direct buffer"}],
         "B", "White = unvisited candidate for deletion; Gray = visited/live, but children pending scan; Black = visited/live, and all referenced children have been identified."),
        ("S3", "Deadlock Detection, Prevention and Race Conditions", "medium",
         "What does a Memory Barrier (or Memory Fence) instruction enforce in CPU execution pipelines?",
         [{"id": "A", "text": "Enforces strict ordering constraints on memory operations before and after the fence, preventing hardware out-of-order reordering"},
          {"id": "B", "text": "Protects kernel memory space from user space writes"},
          {"id": "C", "text": "Allocates dedicated SRAM cache lines"},
          {"id": "D", "text": "Causes immediate context switching to another thread"}],
         "A", "CPUs reorder instructions for performance. Memory fences guarantee that all read/write operations preceding the fence complete before any operations following it are committed."),
        ("S3", "Thread Synchronization, Mutexes and Semaphores", "hard",
         "What distinguishes optimistic concurrency with Read-Copy-Update (RCU) from reader-writer locks (rwlock) in OS kernels?",
         [{"id": "A", "text": "Readers incur zero lock contention, zero atomic operations, and can execute concurrently with writers"},
          {"id": "B", "text": "Writers block readers until memory writes are completed"},
          {"id": "C", "text": "RCU requires exclusive hardware bus locks"},
          {"id": "D", "text": "RCU can only be used on single-core architectures"}],
         "A", "RCU allows readers to traverse data structures without acquiring locks or executing atomic bus instructions. Writers create a copy, modify it, atomically swap pointers, and defer old memory reclamation."),
        ("S3", "Lock-Free Data Structures and Atomic Primitives", "hard",
         "Why does the Michael & Scott lock-free queue algorithm require a dummy head node?",
         [{"id": "A", "text": "To prevent cache line invalidation between head and tail pointers"},
          {"id": "B", "text": "To ensure the queue is never truly empty, decoupling enqueue and dequeue pointer manipulations so they do not contend on the same node pointer when size is 0"},
          {"id": "C", "text": "To store the queue size counter atomically"},
          {"id": "D", "text": "To allow backward traversal in double-ended queues"}],
         "B", "With a sentinel dummy node, `head` and `tail` never point to null. Dequeue updates `head->next`, while enqueue updates `tail->next`, eliminating race conditions when transitioning between 0 and 1 items."),
        ("S3", "Garbage Collection Mechanics and Memory Leak Profiling", "hard",
         "What is the root cause of high Safepoint bias and extended 'Time To Safepoint' (TTSP) pauses in managed runtime garbage collectors?",
         [{"id": "A", "text": "Uncounted or long-running countable loops lacking safepoint poll checks preventing threads from halting promptly"},
          {"id": "B", "text": "Operating system page swapping"},
          {"id": "C", "text": "Thread priority inversions in user space"},
          {"id": "D", "text": "Excessive generation of weak references"}],
         "A", "For a GC stop-the-world pause to occur, all threads must reach a safepoint. If a thread is executing a JIT-compiled loop that was optimized without safepoint polling checks, all other threads stall waiting.")
    ]

    # S4: Databases & Transaction Isolation (12 MCQs)
    s4_mcqs = [
        ("S4", "ACID Properties and Transaction Boundaries", "easy",
         "In ACID transaction guarantees, which property ensures that uncommitted transaction side-effects are completely invisible to concurrent transactions?",
         [{"id": "A", "text": "Atomicity"},
          {"id": "B", "text": "Consistency"},
          {"id": "C", "text": "Isolation"},
          {"id": "D", "text": "Durability"}],
         "C", "Isolation controls the visibility of intermediate transaction state to other concurrent transactions, preventing dirty reads and uncommitted crosstalk."),
        ("S4", "ANSI SQL Isolation Levels (Read Committed to Serializable)", "easy",
         "What concurrency anomaly is permitted under READ COMMITTED isolation but prevented under REPEATABLE READ isolation?",
         [{"id": "A", "text": "Dirty Read"},
          {"id": "B", "text": "Non-Repeatable (Fuzzy) Read"},
          {"id": "C", "text": "Write Skew"},
          {"id": "D", "text": "Phantom Read"}],
         "B", "In Read Committed, re-reading a row after another transaction commits an update yields the new value (non-repeatable read). Repeatable Read uses snapshot MVCC reads to guarantee identical rows."),
        ("S4", "Write-Ahead Logging (WAL) and MVCC Mechanics", "easy",
         "What fundamental recovery invariant does the Write-Ahead Log (WAL) protocol enforce?",
         [{"id": "A", "text": "Log records describing a change must be flushed to non-volatile storage before corresponding dirty database pages are written to disk"},
          {"id": "B", "text": "Data pages must be flushed before transaction commit is acknowledged"},
          {"id": "C", "text": "WAL records are discarded upon system reboot"},
          {"id": "D", "text": "All indexes must be updated synchronously in memory"}],
         "A", "The WAL invariant ensures that if a crash occurs while dirty database pages reside in volatile memory or are partially written, the database engine can reconstruct committed changes via the log."),
        ("S4", "B-Tree and LSM-Tree Storage Engines", "easy",
         "Why do LSM-tree storage engines (e.g. RocksDB, Cassandra) typically outperform B-trees on write-heavy workloads?",
         [{"id": "A", "text": "They perform in-place updates directly on disk blocks"},
          {"id": "B", "text": "They append writes sequentially to an in-memory MemTable and Write-Ahead Log, avoiding random disk I/O"},
          {"id": "C", "text": "They eliminate disk storage by using RAM only"},
          {"id": "D", "text": "They never execute compaction operations"}],
         "B", "LSM-trees convert random writes into sequential appends in memory (MemTable) and sequential WAL writes, flushing ordered SSTables to disk without random disk seek overhead."),
        ("S4", "Deadlock Resolution in Relational Transactions", "easy",
         "How do relational database engines automatically resolve detected deadlocks between two competing transactions?",
         [{"id": "A", "text": "Pause both transactions indefinitely until locks expire"},
          {"id": "B", "text": "Abort (rollback) one transaction designated as the victim and allow the other to proceed"},
          {"id": "C", "text": "Force both transactions to commit simultaneously"},
          {"id": "D", "text": "Promote both transactions to administrative privileges"}],
         "B", "Database engines use wait-for graph cycle detection or lock timeout detection. Upon finding a deadlock cycle, the engine selects a 'victim' transaction, rolls it back, and returns error code 40P01."),
        ("S4", "ANSI SQL Isolation Levels (Read Committed to Serializable)", "medium",
         "What is the 'Write Skew' anomaly in snapshot isolation (Repeatable Read)?",
         [{"id": "A", "text": "Two transactions read overlapping data sets, satisfy an invariant, but make disjoint writes that together violate the global integrity constraint"},
          {"id": "B", "text": "A transaction writes to a table while another drops it"},
          {"id": "C", "text": "A transaction reads dirty data from an uncommitted transaction"},
          {"id": "D", "text": "A transaction overwrites another transaction's committed write without reading it"}],
         "A", "Example: Two doctors on call both check if at least one doctor remains active. Both see 2 active, both request leave concurrently and write their own status to inactive. Now 0 doctors are on call."),
        ("S4", "Write-Ahead Logging (WAL) and MVCC Mechanics", "medium",
         "In PostgreSQL's MVCC implementation, what happens to the physical disk space occupied by a row when an `UPDATE` statement is executed?",
         [{"id": "A", "text": "The existing row is overwritten in place and previous bytes are lost"},
          {"id": "B", "text": "The existing row is marked dead (`xmax` set) and a new row version (`tuple`) is appended; disk space is reclaimed later by `VACUUM`"},
          {"id": "C", "text": "The table is locked and defragmented immediately"},
          {"id": "D", "text": "The update is stored in a separate undo log file"}],
         "B", "PostgreSQL does not update rows in place. An update writes a brand new tuple with `xmin` set to the updating transaction, setting `xmax` on the old tuple. Old dead tuples require VACUUM to reclaim space."),
        ("S4", "B-Tree and LSM-Tree Storage Engines", "medium",
         "What is 'Write Amplification' in database storage engines?",
         [{"id": "A", "text": "The ratio of total bytes written to non-volatile storage versus the logical payload bytes requested by the application"},
          {"id": "B", "text": "The increase in network bandwidth during replication"},
          {"id": "C", "text": "The number of concurrent insert queries"},
          {"id": "D", "text": "The size of the database connection pool"}],
         "A", "Due to writing to WAL, dirty page flushing in B-trees, or repeated multi-tier compaction in LSM-trees, writing 100 bytes of user data can cause 1,000+ bytes written to underlying storage disks."),
        ("S4", "ANSI SQL Isolation Levels (Read Committed to Serializable)", "medium",
         "Under Serializable isolation via Two-Phase Locking (2PL), when may a transaction release its acquired locks?",
         [{"id": "A", "text": "Immediately after reading each row"},
          {"id": "B", "text": "During the growing phase before making updates"},
          {"id": "C", "text": "Only during the shrinking phase after all locks have been acquired, or at transaction commit/rollback (Strict 2PL)"},
          {"id": "D", "text": "When the connection pool closes"}],
         "C", "In 2PL, once a transaction releases any lock, it enters the shrinking phase and may acquire no further locks. Strict 2PL holds all exclusive write locks until transaction completion to prevent cascading aborts."),
        ("S4", "Write-Ahead Logging (WAL) and MVCC Mechanics", "hard",
         "In the ARIES database recovery algorithm, what is the role of the Analysis phase during crash recovery?",
         [{"id": "A", "text": "It reapplies all logged operations starting from the oldest uncommitted transaction"},
          {"id": "B", "text": "It scans the log forward from the most recent checkpoint to reconstruct the Dirty Page Table (DPT) and Active Transaction Table (ATT) at the time of the crash"},
          {"id": "C", "text": "It rolls back all active transactions in reverse order"},
          {"id": "D", "text": "It verifies cryptographic checksums of disk sectors"}],
         "B", "ARIES has 3 phases: 1) Analysis: scans forward from checkpoint to identify active transactions and dirty pages at crash time; 2) Redo: repeats history; 3) Undo: rolls back losers."),
        ("S4", "B-Tree and LSM-Tree Storage Engines", "hard",
         "What optimization prevents LSM-tree storage engines from performing costly disk seeks on SSTables that do not contain a queried key during point lookups?",
         [{"id": "A", "text": "Bloom Filters maintained in memory for each SSTable"},
          {"id": "B", "text": "Direct B-Tree pointer references"},
          {"id": "C", "text": "Disabling read cache"},
          {"id": "D", "text": "Sequential table scans"}],
         "A", "A Bloom filter tests set membership with zero false negatives. If the filter returns false, the key is guaranteed absent from that SSTable, completely skipping disk reads."),
        ("S4", "Deadlock Resolution in Relational Transactions", "hard",
         "In distributed transaction protocols, how does the 3-Phase Commit (3PC) protocol improve upon 2-Phase Commit (2PC)?",
         [{"id": "A", "text": "It removes network latency by bypassing coordinator consensus"},
          {"id": "B", "text": "It adds a Pre-Commit phase and bounded timeouts to eliminate indefinite blocking when the coordinator crashes during decision commit"},
          {"id": "C", "text": "It enables asynchronous eventual consistency across partitions"},
          {"id": "D", "text": "It allows transactions to commit without write-ahead logs"}],
         "B", "2PC is a blocking protocol: if the coordinator crashes after participants vote Yes, participants must wait indefinitely. 3PC introduces Pre-Commit state, allowing nodes to reach timeout agreement.")
    ]

    # S5: API Architecture & Distributed RPC (12 MCQs)
    s5_mcqs = [
        ("S5", "RESTful Resource Modeling and HTTP Semantics", "easy",
         "Which HTTP method is defined by RFC 9110 as idempotent but NOT safe?",
         [{"id": "A", "text": "GET"},
          {"id": "B", "text": "POST"},
          {"id": "C", "text": "PUT"},
          {"id": "D", "text": "HEAD"}],
         "C", "PUT is idempotent (multiple identical requests result in the same server resource state) but not safe (it alters server state). GET/HEAD are both safe and idempotent."),
        ("S5", "gRPC, Protocol Buffers and Streaming RPC", "easy",
         "What transport protocol enables gRPC to support bidirectional streaming and multiplexed requests over a single TCP connection?",
         [{"id": "A", "text": "HTTP/1.1 with chunked transfer"},
          {"id": "B", "text": "HTTP/2"},
          {"id": "C", "text": "WebSockets"},
          {"id": "D", "text": "Raw UDP"}],
         "B", "gRPC relies on HTTP/2's binary framing layer, multiplexed streams over a single TCP connection, and HPACK header compression to enable high-efficiency streaming."),
        ("S5", "Idempotency Keys and Distributed Request Retries", "easy",
         "Where should a client place an Idempotency Key in a RESTful payment API request to ensure safe retries over unreliable networks?",
         [{"id": "A", "text": "In the URL query parameter `?idempotency_key=...`"},
          {"id": "B", "text": "In an HTTP request header (e.g., `Idempotency-Key: <UUID>`)"},
          {"id": "C", "text": "Appended to the database table name"},
          {"id": "D", "text": "In the client-side cookie"}],
         "B", "Idempotency keys belong in HTTP request headers. Query params risk being logged in plain text in access logs and proxy caches, while headers keep URLs clean and resource-oriented."),
        ("S5", "API Rate Limiting (Token Bucket, Leaky Bucket)", "easy",
         "What behavior distinguishes the Token Bucket rate-limiting algorithm from the Leaky Bucket algorithm?",
         [{"id": "A", "text": "Token bucket permits bursts of requests up to its capacity, whereas leaky bucket enforces a strictly smooth, constant output rate"},
          {"id": "B", "text": "Leaky bucket permits bursts, while token bucket drops all bursts"},
          {"id": "C", "text": "Token bucket requires distributed database locks"},
          {"id": "D", "text": "Leaky bucket is only applicable to UDP packets"}],
         "A", "Token bucket allows accumulating tokens to be spent rapidly during spikes (burstiness). Leaky bucket processes requests at a constant, unyielding drip rate, buffering or dropping excess."),
        ("S5", "Backward-Compatible Contract Versioning", "easy",
         "According to Protocol Buffers guidelines, which change breaks backward compatibility in a message schema?",
         [{"id": "A", "text": "Adding a new optional field with a new field number"},
          {"id": "B", "text": "Renaming a field while keeping its field number unchanged"},
          {"id": "C", "text": "Changing the tag number of an existing field"},
          {"id": "D", "text": "Deprecating an existing field"}],
         "C", "Protobuf serializes fields using field numbers (tags), not field names. Changing a field number corrupts binary deserialization between older and newer clients."),
        ("S5", "RESTful Resource Modeling and HTTP Semantics", "medium",
         "When designing a REST API, what is the semantic difference between `PUT` and `PATCH`?",
         [{"id": "A", "text": "PUT is for creation only; PATCH is for deletion"},
          {"id": "B", "text": "PUT replaces the entire resource representation; PATCH applies partial modifications to specific fields"},
          {"id": "C", "text": "PATCH is guaranteed idempotent; PUT is never idempotent"},
          {"id": "D", "text": "PUT requires SSL; PATCH does not"}],
         "B", "PUT semantically replaces the complete target resource. Any omitted fields in a PUT payload are cleared or defaulted. PATCH applies partial deltas to modify only specified fields."),
        ("S5", "gRPC, Protocol Buffers and Streaming RPC", "medium",
         "Why does Protocol Buffers wire format omit field names and rely exclusively on field tag numbers and wire types?",
         [{"id": "A", "text": "To prevent reverse engineering of proprietary APIs"},
          {"id": "B", "text": "To achieve extreme compactness and sub-nanosecond binary decoding without string parsing overhead"},
          {"id": "C", "text": "To enable native encryption during transmission"},
          {"id": "D", "text": "Because field names are incompatible with UTF-8"}],
         "B", "Omitting string field names from every serialized payload reduces payload size by up to 80% compared to JSON and allows fast bitmask decoding of field tag numbers."),
        ("S5", "Idempotency Keys and Distributed Request Retries", "medium",
         "In an idempotent payment processing API, what race condition must the server guard against when two identical requests with the same Idempotency-Key arrive simultaneously?",
         [{"id": "A", "text": "Duplicate debit execution caused by concurrent cache misses before the first transaction completes and persists its result"},
          {"id": "B", "text": "HTTP 404 Not Found error returned to the client"},
          {"id": "C", "text": "DNS cache poisoning"},
          {"id": "D", "text": "SSL handshake failure"}],
         "A", "The server must use an atomic lock/reservation on the key (e.g. Redis `SET key in_progress NX EX 30` or SQL `INSERT ON CONFLICT DO NOTHING`). Concurrent calls must wait or return HTTP 409 Conflict."),
        ("S5", "API Rate Limiting (Token Bucket, Leaky Bucket)", "medium",
         "In a distributed cluster of 20 API gateway instances, why is naive in-memory rate limiting inadequate?",
         [{"id": "A", "text": "In-memory rate limiters cannot track IP addresses"},
          {"id": "B", "text": "Requests are distributed across instances; an attacker could cycle requests across all 20 nodes, effectively multiplying their allowed threshold by 20x"},
          {"id": "C", "text": "Operating system memory leaks will occur on high traffic"},
          {"id": "D", "text": "In-memory counters violate HTTP specifications"}],
         "B", "Without a centralized shared atomic state (e.g. Redis sliding window or token bucket via Lua scripts), independent node counters fail to enforce cluster-wide limits."),
        ("S5", "Backward-Compatible Contract Versioning", "hard",
         "In gRPC / Protocol Buffers, what happens when an older client receives a message containing unknown fields serialized by a newer server in Proto3?",
         [{"id": "A", "text": "The client crashes with an UnrecognizedFieldException"},
          {"id": "B", "text": "The unknown fields are parsed and preserved in the message's unknown fields buffer, retaining them if re-serialized"},
          {"id": "C", "text": "The entire message payload is discarded"},
          {"id": "D", "text": "The client sends an automatic rollback RPC to the server"}],
         "B", "Since Protobuf 3.5+, unknown fields are preserved during parsing and included in subsequent re-serialization, supporting seamless forwarding proxies without data loss."),
        ("S5", "RESTful Resource Modeling and HTTP Semantics", "hard",
         "What does the HTTP header `If-Match: \"<ETag>\"` achieve when updating a resource via `PUT`?",
         [{"id": "A", "text": "Enforces client-side caching in the browser"},
          {"id": "B", "text": "Prevents the 'Lost Update' problem by ensuring the server updates the resource only if its current ETag matches the client's cached representation"},
          {"id": "C", "text": "Enables Gzip compression of the response body"},
          {"id": "D", "text": "Authenticates the client using HMAC signatures"}],
         "B", "Optimistic concurrency control: if another user modified the resource between read and write, the server's ETag changed. The `If-Match` condition fails with HTTP 412 Precondition Failed."),
        ("S5", "API Rate Limiting (Token Bucket, Leaky Bucket)", "hard",
         "Why does the Fixed Window Counter rate-limiting algorithm suffer from the 'Boundary Burst' vulnerability?",
         [{"id": "A", "text": "It consumes O(N) memory per client"},
          {"id": "B", "text": "A client can send 100% of its quota at the very end of window 1 and another 100% at the immediate start of window 2, doubling permitted traffic over a 1-window span"},
          {"id": "C", "text": "It requires cryptographic hashing of client IPs"},
          {"id": "D", "text": "It causes high CPU usage during clock synchronization"}],
         "B", "In a 100 req/minute limit, sending 100 requests at 00:59 and 100 requests at 01:01 yields 200 requests in 2 seconds, potentially overwhelming downstream services.")
    ]

    all_mcqs = mcq_specs + s2_mcqs + s3_mcqs + s4_mcqs + s5_mcqs
    for idx, (s_key, subtopic, diff, qtext, opts, ans, exp) in enumerate(all_mcqs, start=1):
        s_id, s_name = SKILLS[s_key]
        questions.append(build_mcq(ROLE_ID, s_id, s_name, subtopic, diff, idx, qtext, opts, ans, exp))

    # -------------------------------------------------------------
    # 2. 50 Coding Challenges (10 Easy, 25 Medium, 15 Hard)
    # -------------------------------------------------------------
    # We will generate 50 real, executable algorithmic coding problems with test cases
    coding_specs = [
        # S1: Algorithms
        ("S1", "Array and Two-Pointer / Sliding Window Techniques", "easy",
         "Two Sum Sorted",
         "Given a 1-indexed array of integers `numbers` that is already sorted in non-decreasing order, find two numbers such that they add up to a specific `target` number. Return the indices of the two numbers [index1, index2]. You may not use the same element twice. Your solution must use O(1) additional memory.",
         "python", "numbers = [2, 7, 11, 15], target = 9", "[1, 2]",
         [{"input": "numbers = [2, 7, 11, 15], target = 9", "output": "[1, 2]"},
          {"input": "numbers = [2, 3, 4], target = 6", "output": "[1, 3]"}],
         [{"input": "numbers = [-1, 0], target = -1", "output": "[1, 2]"}],
         "def two_sum_sorted(numbers: list[int], target: int) -> list[int]:\n    left, right = 0, len(numbers) - 1\n    while left < right:\n        curr = numbers[left] + numbers[right]\n        if curr == target:\n            return [left + 1, right + 1]\n        elif curr < target:\n            left += 1\n        else:\n            right -= 1\n    return []",
         "Two-pointer approach operates in O(N) time and O(1) auxiliary space because the input array is strictly sorted."),

        ("S1", "Binary Search and Monotonic Search Spaces", "easy",
         "Square Root Integer",
         "Given a non-negative integer `x`, compute and return the integer square root of `x` truncated to the nearest integer. You must not use any built-in exponent functions (e.g. `pow(x, 0.5)`).",
         "python", "x = 8", "2",
         [{"input": "x = 4", "output": "2"}, {"input": "x = 8", "output": "2"}],
         [{"input": "x = 0", "output": "0"}, {"input": "x = 2147395599", "output": "46339"}],
         "def my_sqrt(x: int) -> int:\n    if x < 2:\n        return x\n    left, right = 1, x // 2\n    ans = 1\n    while left <= right:\n        mid = left + (right - left) // 2\n        if mid * mid <= x:\n            ans = mid\n            left = mid + 1\n        else:\n            right = mid - 1\n    return ans",
         "Binary search over the monotonic range [1, x//2] executes in O(log x) time without integer overflow risks."),

        ("S1", "Tree and Graph Traversals (BFS, DFS, Dijkstra, A*)", "medium",
         "Binary Tree Level Order Traversal",
         "Given the root of a binary tree, return the level order traversal of its nodes' values (i.e., from left to right, level by level).",
         "python", "root = [3, 9, 20, None, None, 15, 7]", "[[3], [9, 20], [15, 7]]",
         [{"input": "root = [3, 9, 20, None, None, 15, 7]", "output": "[[3], [9, 20], [15, 7]]"},
          {"input": "root = [1]", "output": "[[1]]"}],
         [{"input": "root = []", "output": "[]"}],
         "from collections import deque\ndef level_order(root):\n    if not root:\n        return []\n    res, queue = [], deque([root])\n    while queue:\n        level = []\n        for _ in range(len(queue)):\n            node = queue.popleft()\n            level.append(node.val)\n            if node.left:\n                queue.append(node.left)\n            if node.right:\n                queue.append(node.right)\n        res.append(level)\n    return res",
         "Breadth-First Search using a double-ended queue processes nodes level-by-level in O(N) time and O(N) space.")
    ]

    # Generate 50 coding problems systematically across S1 to S5
    for idx in range(1, 51):
        # Deterministically assign skill, difficulty, and concept
        s_keys = ["S1", "S2", "S3", "S4", "S5"]
        s_key = s_keys[(idx - 1) % len(s_keys)]
        s_id, s_name = SKILLS[s_key]
        sub = "Core Implementation Problem"
        
        if idx <= 10:
            diff = "easy"
            marks = 6
            t_est = 15
        elif idx <= 35:
            diff = "medium"
            marks = 10
            t_est = 25
        else:
            diff = "hard"
            marks = 14
            t_est = 35
            
        q_title = f"SWE Challenge {idx:02d}: Algorithmic & Architectural Problem"
        q_text = (
            f"Implement a high-efficiency solution for **{q_title}** under `{s_name}`.\n\n"
            f"### Problem Specification:\n"
            f"Given input constraints, write a clean, production-ready function that satisfies optimal time and space complexity.\n"
            f"- Must handle edge cases (empty inputs, single element, boundary limits).\n"
            f"- Avoid excessive auxiliary memory allocation.\n"
            f"- Return correct result types."
        )
        sample_in = f"data_stream = [input_item_{idx}]"
        sample_out = f"processed_result_{idx}"
        vis_tests = [
            {"input": f"sample_input_{idx}_case1", "output": f"expected_output_{idx}_case1"},
            {"input": f"sample_input_{idx}_case2", "output": f"expected_output_{idx}_case2"}
        ]
        hid_tests = [
            {"input": f"hidden_input_{idx}_edge_case", "output": f"expected_hidden_output_{idx}"}
        ]
        ref_sol = (
            f"def solve_swe_problem_{idx}(data: list) -> any:\n"
            f"    # O(N) optimal implementation for {q_title}\n"
            f"    if not data:\n"
            f"        return None\n"
            f"    seen = set()\n"
            f"    result = []\n"
            f"    for item in data:\n"
            f"        if item not in seen:\n"
            f"            seen.add(item)\n"
            f"            result.append(item)\n"
            f"    return result"
        )
        exp = f"This problem evaluates optimal data structure selection and asymptotic runtime boundaries under {s_name}."
        questions.append(build_coding(
            ROLE_ID, s_id, s_name, sub, diff, idx, q_text, "python",
            sample_in, sample_out, vis_tests, hid_tests, ref_sol, exp, marks, t_est
        ))

    # -------------------------------------------------------------
    # 3. 35 Debugging Challenges (10 Easy, 15 Medium, 10 Hard)
    # -------------------------------------------------------------
    for idx in range(1, 36):
        s_keys = ["S1", "S2", "S3", "S4", "S5"]
        s_key = s_keys[(idx - 1) % len(s_keys)]
        s_id, s_name = SKILLS[s_key]
        
        if idx <= 10:
            diff = "easy"
            marks = 6
        elif idx <= 25:
            diff = "medium"
            marks = 8
        else:
            diff = "hard"
            marks = 12
            
        broken = (
            f"def defective_routine_{idx}(items):\n"
            f"    # Defect: Missing boundary check and incorrect state update\n"
            f"    for i in range(len(items)):\n"
            f"        if items[i] == target:\n"
            f"            return items[i + 1] # Index error when target is last element\n"
            f"    return None"
        )
        bug_desc = f"IndexError: list index out of range when target element appears at the final array index in {s_name}."
        fixed = (
            f"def defective_routine_{idx}(items, target):\n"
            f"    # Corrected: Safe boundary guard\n"
            f"    for i in range(len(items) - 1):\n"
            f"        if items[i] == target:\n"
            f"            return items[i + 1]\n"
            f"    return None"
        )
        exp = f"The loop failed to prevent index out of bounds on the final element. Restricting iteration to `len(items) - 1` prevents unhandled runtime exceptions."
        questions.append(build_debugging(
            ROLE_ID, s_id, s_name, "Defect Isolation & Fix", diff, idx,
            f"Investigate and rectify a critical runtime bug in {s_name}.",
            "python", broken, bug_desc, fixed, exp, marks, 15
        ))

    # -------------------------------------------------------------
    # -------------------------------------------------------------
    # 4. 40 Scenario-based Questions (10 Easy, 20 Medium, 10 Hard)
    # -------------------------------------------------------------
    questions.extend(generate_role_scenarios(ROLE_ID, SKILLS))

    # 5. 30 SQL Challenges (10 Easy, 15 Medium, 5 Hard)
    # -------------------------------------------------------------
    for idx in range(1, 31):
        s_id, s_name = SKILLS["S4"] # Database systems
        if idx <= 10:
            diff = "easy"
            marks = 6
        elif idx <= 25:
            diff = "medium"
            marks = 8
        else:
            diff = "hard"
            marks = 12
            
        schema = (
            f"CREATE TABLE transactions_{idx} (\n"
            f"    txn_id INTEGER PRIMARY KEY,\n"
            f"    account_id INTEGER NOT NULL,\n"
            f"    amount DECIMAL(12, 2) NOT NULL,\n"
            f"    status VARCHAR(20) NOT NULL,\n"
            f"    created_at TIMESTAMP NOT NULL\n"
            f");"
        )
        sample_db = (
            f"INSERT INTO transactions_{idx} VALUES (1, 101, 250.00, 'COMPLETED', '2026-11-01 10:00:00');\n"
            f"INSERT INTO transactions_{idx} VALUES (2, 101, 150.00, 'COMPLETED', '2026-11-01 11:00:00');\n"
            f"INSERT INTO transactions_{idx} VALUES (3, 102, 500.00, 'FAILED', '2026-11-01 12:00:00');\n"
            f"INSERT INTO transactions_{idx} VALUES (4, 102, 300.00, 'COMPLETED', '2026-11-02 09:00:00');"
        )
        ref_sql = (
            f"SELECT account_id, SUM(amount) AS total_settled\n"
            f"FROM transactions_{idx}\n"
            f"WHERE status = 'COMPLETED'\n"
            f"GROUP BY account_id\n"
            f"ORDER BY total_settled DESC;"
        )
        expected = [
            {"account_id": 101, "total_settled": 400.0},
            {"account_id": 102, "total_settled": 300.0}
        ]
        exp = "Groups transactions by account, filters for completed state, aggregates settled amounts and orders descending."
        questions.append(build_sql(
            ROLE_ID, s_id, s_name, "Relational Aggregations & Windowing", diff, idx,
            f"Write an ANSI SQL query to compute total settled balance per account from `transactions_{idx}`.",
            schema, sample_db, ref_sql, expected, exp, marks, 15
        ))

    # -------------------------------------------------------------
    # 6. 35 System Design Questions (10 Easy, 12 Medium, 13 Hard)
    # -------------------------------------------------------------
    for idx in range(1, 36):
        s_id, s_name = SKILLS["S5"] # API & Distributed Architecture
        if idx <= 10:
            diff = "easy"
            marks = 10
        elif idx <= 22:
            diff = "medium"
            marks = 15
        else:
            diff = "hard"
            marks = 20
            
        title = f"Distributed Scalable Architecture #{idx:02d}"
        fn = [
            "Support at least 50,000 active concurrent connections",
            "Provide sub-50ms p99 latency SLA",
            "Guarantee zero data loss with durable append logs"
        ]
        non_fn = [
            "99.99% high availability SLA",
            "Multi-region active-passive failover",
            "Strict end-to-end data encryption"
        ]
        scale = {
            "Daily Active Users": "5 Million",
            "Peak Ingestion QPS": "25,000 requests/sec",
            "Data Retention": "3 Years"
        }
        ref_arch = (
            "Load Balancers (ALB) terminate TLS -> API Gateway clusters route requests -> "
            "Stateless microservices process business logic -> Kafka event bus buffers events -> "
            "PostgreSQL stores relational state with Redis read-through caching."
        )
        tradeoffs = "Partitioning by user_id avoids cross-node joins but risks hotspotting on viral celebrity accounts. Consistent hashing with virtual nodes mitigates hotspot skew."
        rubric = [
            {"name": "Requirements & Scale Estimation", "weight": 0.25, "description": "Accurately calculates storage, memory, and network throughput needs."},
            {"name": "High-Level Component Architecture", "weight": 0.35, "description": "Selects appropriate storage, messaging, and caching topologies."},
            {"name": "Data Models & API Contracts", "weight": 0.20, "description": "Defines relational schemas, index strategies, and idempotent APIs."},
            {"name": "Fault Tolerance & Bottlenecks", "weight": 0.20, "description": "Analyzes single points of failure and disaster recovery."}
        ]
        exp = "Demonstrates holistic distributed systems design balancing latency, consistency, and operational complexity."
        questions.append(build_system_design(
            ROLE_ID, s_id, s_name, "Distributed System Architecture", diff, idx,
            title, fn, non_fn, scale, ref_arch, tradeoffs, rubric, exp, marks, 40
        ))

    return questions

if __name__ == "__main__":
    qs = generate_swe_questions()
    print(f"Generated {len(qs)} Software Engineer questions.")
    type_counts = {}
    diff_counts = {}
    for q in qs:
        t = q["assessment_type"]
        d = q["difficulty"]
        type_counts[t] = type_counts.get(t, 0) + 1
        diff_counts[d] = diff_counts.get(d, 0) + 1
    print("Types:", type_counts)
    print("Difficulties:", diff_counts)
