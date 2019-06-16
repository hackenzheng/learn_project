class Solution:
    def IsBalanced_Solution(self, pRoot):
        # write code here
        return self.deepth(pRoot) != -1

    def deepth(self, pRoot):
        # 返回树的高度，不平衡的情况为-1，空节点是0
        if not pRoot:
            return 0
        if not pRoot.left and not pRoot.right:
            return 1
        left = self.deepth(pRoot.left)
        right = self.deepth(pRoot.right)
        if left == -1 or right == -1:
            return -1
        if left - right > 1 or left - right < -1:
            return -1
        else:
            return max(left + 1, right + 1)