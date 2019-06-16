//
// Created by zhg on 19-4-12.
// 判断二叉树是否是镜像的
//

/*
struct TreeNode {
    int val;
    struct TreeNode *left;
    struct TreeNode *right;
    TreeNode(int x) :
            val(x), left(NULL), right(NULL) {
    }
};
*/
class Solution {
public:
    bool isSymmetrical(TreeNode* pRoot)
    {
       //定义遍历方式， 根节点左节点右节点， 根节点右节点左节点， 两种遍历方式要是一样的
       return isSymmetricalCore(pRoot, pRoot)
    }

    bool isSymmetricalCore(TreeNode* p1, TreeNode* p2)
    {

    }

};

