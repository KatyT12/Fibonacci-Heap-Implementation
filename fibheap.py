class FibNode:
    def __init__(self,payload,key):
        self.payload = payload
        self.key = key
        self.loser = False

        self.is_root = True
        self.parent = None
        self.left = None
        self.child = None
        self.right = None
        self.degree = 0


class FibHeap:
    def __init__(self):
        self.min = None
        self.roots = []
        self.vertices = {}

    def push(self,x,k):
        # O(1)
        if x in self.vertices:
            raise ValueError(f"push item {x} which is already in the heap")
        print("Pushing ", k)
        node = FibNode(x,k)
        self.vertices[x] = node
        self.roots.append(node) # Attention

        if self.min == None or self.min.key > k:
            self.min = node

    def moveToRoot(self,n):
        if n.right != None:
            n.right.left = n.left
        if n.left != None:
            n.left.right = n.right
        if n.parent != None:
            if n.parent.child == n:
                n.parent.child = n.right
            n.parent.degree -= 1
        n.parent = None
        n.left = None
        n.right = None
        n.loser = False
        n.is_root = True
        self.roots.append(n)


    def decreasekey(self, x, k):
        # Decrease key

        n = self.vertices[x]
        print("Decreasing ", n.key, k)
        n.key = k

        # Check if min
        if k < self.min.key:
            self.min = n

        if not n.is_root:
            if n.parent.key > n.key:
                # Have to deal with this
                n.is_root = True

                p = n.parent # Before n.parent gets set to None
                self.moveToRoot(n)

                while p.loser and not (p.is_root):
                    parent = p.parent
                    self.moveToRoot(p)
                    p = parent

                if not p.is_root:
                    p.loser = True

    def merge(self,n1,n2, bool = False):
        #if n1.key == 86:
            #print([v.key for v in self.roots])
        parent = n1
        child = n2
        if n2.key < n1.key or bool:
            parent = n2
            child = n1

        child.parent = parent
        if parent.child == None:
            parent.child = child
        else: # Add to the right
            temp = parent.child.right
            parent.child.right = child
            child.right = temp
            child.left = parent.child
            if temp != None:
                temp.left = child
        child.is_root = False
        parent.degree += 1
        #self.roots.remove(child)

        return parent

    def cleanup(self):
        minroot = None
        min = float('Inf')
        root_array = {}
        for t in self.roots:
            x = t
            if t.key < min:
                min = t.key
                minroot = t
            while root_array.get(x.degree) != None:
                u = root_array[x.degree]
                root_array[x.degree] = None
                x = self.merge(u,x,x == minroot)
            root_array[x.degree] = x
        ret = [ v for v in root_array.values() if v != None]
        #if len(ret) >= 3:
           # print([v.key for v in ret], [v.key for v in self.roots])
        return ret,minroot

    def popmin(self):
        print("Popping min ","Value = ", self.min.payload , " Key= ", self.min.key)
        if self.min.key == 83:
            print([v.key for v in self.roots])

        minroot = self.min
        if not self.min.is_root:
            print(self.min.parent.key, self.min.parent.is_root)

        self.roots.remove(self.min)
        self.vertices.pop(minroot.payload)

        # Promote children to be roots
        pointer = minroot.child
        while pointer != None:
            self.moveToRoot(pointer)
            pointer = minroot.child
        # Do cleanup and update minroot
        self.roots,self.min = self.cleanup()
        return minroot.payload

    def __bool__(self):
        return len(self.roots) > 0

    def __contains__(self,x):
        return x in self.vertices

class Vertex:
    def __init__(self, id):
        self.id = id
        self.distance = None
    def __str__(self):
        return f"vertex({self.id})"

def dijkstra(g, s):
    for v in g:
        v.distance = float('inf')
    s.distance = 0

    toexplore = FibHeap()
    toexplore.push(s, s.distance)

    while toexplore:
        v = toexplore.popmin()
        for w,edgecost in g[v]:
            dist_w = v.distance + edgecost
            if dist_w < w.distance:
                w.distance = dist_w
                if w in toexplore:
                    toexplore.decreasekey(w, w.distance)
                else:
                    toexplore.push(w, w.distance)


# Testing/Debugging
if __name__ == "__main__":
    heap = FibHeap()
    heap.push(0,16)
    heap.push(1, 46)
    heap.push(2, 45)
    heap.push(3, 11)
    heap.push(4, 44)
    heap.push(5, 47)
    heap.push(6, 21)
    heap.push(7, 2)
    heap.push(8, 18)
    heap.push(9, 25)
    n = heap.popmin()
    print(n)
    heap.push(10,51)
    heap.decreasekey(5,24)
    heap.decreasekey(6,11)
    n = heap.popmin()
    print(n)
    heap.push(11,47)
    n = heap.popmin()
    print(n)
    heap.popmin()
    heap.push(12,47)
    heap.popmin()
    heap.push(13,32)
    heap.decreasekey(4,11)
    heap.popmin()

#Popping min  Value =  45  Key=  74