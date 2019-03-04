# DFS、BFS



## [22. Generate Parentheses](https://leetcode.com/problems/generate-parentheses/)

```java
class Solution {
    public List<String> generateParenthesis(int n) {
        List<String> res = new ArrayList<>();
        if (n < 1) {
            return res;
        }
        StringBuilder cur = new StringBuilder();
        generateParenthesisHelper(n, n, cur, res);
        return res;
    }
    
    private void generateParenthesisHelper(int left, int right, StringBuilder cur, List<String> res) {
        if (left == 0 && right == 0) {
            res.add(cur.toString());
            return;
        }
        if (0 < left && left <= right) {
            cur.append('(');
            generateParenthesisHelper(left - 1, right, cur, res);
            cur.deleteCharAt(cur.length() - 1);
        }
        if (0 < right) {
            cur.append(')');
            generateParenthesisHelper(left, right - 1, cur, res);
            cur.deleteCharAt(cur.length() - 1);
        }
    }
}
```

