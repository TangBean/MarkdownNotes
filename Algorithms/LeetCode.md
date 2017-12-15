---
style: ocean
---
LeetCode
===
[[TOC]]

# Array

## 118. Pascal's Triangle

#### 原题地址
[https://leetcode.com/problems/pascals-triangle/description/](https://leetcode.com/problems/pascals-triangle/description/)

#### 题目
> Given _numRows_, generate the first _numRows_ of Pascal's triangle.
> For example, given _numRows_ = 5,
> Return
> [ [1], [1,1], [1,2,1], [1,3,3,1], [1,4,6,4,1] ]

#### 思路

#### 代码
```java
class Solution {
    public List<List<Integer>> generate(int numRows) {
        List<List<Integer>> ans = new ArrayList<List<Integer>>(numRows);
        ArrayList arr = new ArrayList<Integer>();
        for (int i = 0; i < numRows; i++) {
            arr.add(0, 1);
            for (int j = 1; j < arr.size()-1; j++)
                arr.set(j, ans.get(i-1).get(j-1) + ans.get(i-1).get(j));
            ans.add(new ArrayList<Integer>(arr));
        }
        return ans;
    }
}
```

## 167. Two Sum II - Input array is sorted

#### 原题地址
[https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/description/](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/description/)

#### 题目
> Given an array of integers that is already **_sorted in ascending order_**, find two numbers such that they add up to a specific target number.
> The function twoSum should return indices of the two numbers such that they add up to the target, where index1 must be less than index2\. Please note that your returned answers (both index1 and index2) are not zero-based.
> You may assume that each input would have _exactly_ one solution and you may not use the _same_ element twice.
> **Input:** numbers={2, 7, 11, 15}, target=9
> **Output:** index1=1, index2=2

#### 思路
- 两个指针分别指向首尾
- 如果比`target`小，前面的指针后移，如果比`target`大，后面的指针前移


## 169. Majority Element

#### 原题地址
[https://leetcode.com/problems/majority-element/description/](https://leetcode.com/problems/majority-element/description/)

#### 题目
> Given an array of size _n_, find the majority element. The majority element is the element that appears **more than** `⌊ n/2 ⌋` times.
> You may assume that the array is non-empty and the majority element always exist in the array.
> 就是求众数

#### 思路
- 不停的剪前缀的方法，设置一个`count`一个`maj`，让`maj`等于数组第一个元素，然后向后扫描，相同`count++`，不同`count--`，`count`变成0就剪一次前缀


##  189. Rotate Array

#### 原题地址
[https://leetcode.com/problems/rotate-array/description/](https://leetcode.com/problems/rotate-array/description/)

#### 题目
> Rotate an array of _n_ elements to the right by _k_ steps.
> For example, with _n_ = 7 and _k_ = 3, the array `[1,2,3,4,5,6,7]` is rotated to `[5,6,7,1,2,3,4]`.

#### 思路
- 奇妙的方法
	- `reverse(0, n-1);`
	- `reverse(0, k-1);`
	- `reverse(k, n-1);`


## 55. Jump Game

#### 原题链接
[https://leetcode.com/problems/jump-game/description/](https://leetcode.com/problems/jump-game/description/)

#### 题目
> Given an array of non-negative integers, you are initially positioned at the first index of the array.
> Each element in the array represents your maximum jump length at that position.
> Determine if you are able to reach the last index.
> For example:
> A = [2,3,1,1,4], return true.
> A = [3,2,1,0,4], return false.

#### 思路
- 定义一个变量保存当前能到达的最远距离`maxStep`
- 每移动一步，就比较`maxStep = Math.max(i+nums[i], maxStep)`
- 当遇到0时，如果最远距离就在当前位置，返回`false`

#### 代码
```java
public boolean canJump(int[] nums) {
	int maxStep = 0;
	for (int i = 0; maxStep < nums.length-1; i++) {
		if (nums[i] == 0 && maxStep == i) return false;
		int nextMaxStep = i + nums[i];
		if (nextMaxStep > maxStep) maxStep = nextMaxStep;
	}
	return true;
}
```

## 15. 3Sum

#### 原题链接
[https://leetcode.com/problems/3sum/description/](https://leetcode.com/problems/3sum/description/)

#### 题目
> Given an array S of n integers, are there elements a, b, c in S such that a + b + c = 0? Find all unique triplets in the array which gives the sum of zero.
> For example, given array S = [-1, 0, 1, 2, -1, -4],
> A solution set is:
> [
>   [-1, 0, 1],
>   [-1, -1, 2]
> ]

#### 思路
- 先对数组进行排序`Arrays.sort(nums)`
- 两趟循环，头指针，尾指针，跳过重复元素

#### 代码
```java
public List<List<Integer>> threeSum(int[] nums) {
	Arrays.sort(nums);
	List<List<Integer>> ans = new ArrayList<List<Integer>>();
	for (int i = 0; i < nums.length-2; i++) {
		if (i == 0 || (i > 0 && nums[i] != nums[i-1])) {
			int lo = i + 1, hi = nums.length-1, sum = 0 - nums[i];
			while (lo < hi) {
				if (nums[lo] + nums[hi] == sum) {
					ans.add(Arrays.asList(nums[i], nums[lo], nums[hi]));
					while(lo < hi && nums[lo] == nums[++lo]);
					while(lo < hi && nums[hi] == nums[--hi]);
				}
				else if (nums[lo] + nums[hi] < sum) lo++;
				else hi--;
			}
		}
	}
	return ans;
}
```

## 16. 3Sum Closest

#### 原题链接
[https://leetcode.com/problems/3sum-closest/description/](https://leetcode.com/problems/3sum-closest/description/)

#### 题目
> Given an array _S_ of _n_ integers, find three integers in _S_ such that the sum is closest to a given number, target. Return the sum of the three integers. You may assume that each input would have exactly one solution.
> For example, given array S = {-1 2 1 -4}, and target = 1.
> The sum that is closest to the target is 2\. (-1 + 2 + 1 = 2).

#### 思路
- 和上道题差不多，也是先排序

#### 代码
```java
public int threeSumClosest(int[] nums, int target) {
	Arrays.sort(nums);
	int ans = nums[0] + nums[1] + nums[2];
	int lo, hi;
	for (int i = 0; i < nums.length-2; i++) {
	    lo = i + 1;
	    hi = nums.length - 1;
	    while (lo < hi) {
	        int sum = nums[i] + nums[lo] + nums[hi];
	        if (sum < target) lo++;
	        else hi--;
	        if (Math.abs(sum - target) < Math.abs(ans - target)) ans = sum;
	    }
	}
	return ans;
}
```

## 59. Spiral Matrix II

#### 原题链接
[https://leetcode.com/problems/spiral-matrix-ii/discuss/](https://leetcode.com/problems/spiral-matrix-ii/discuss/)

#### 题目
> Given an integer _n_, generate a square matrix filled with elements from 1 to _n_2 in spiral order.
> For example,
> Given _n_ = `3`,
> You should return the following matrix:
> [
>  [ 1, 2, 3 ],
>  [ 8, 9, 4 ],
>  [ 7, 6, 5 ]
> ]

#### 思路
- 设置4个指针，`left`, `right`, `top`, `down`

#### 代码
```java
public int[][] generateMatrix(int n) {
	int[][] res = new int[n][n];
    int num = 1;
    for(int layer=0; layer<(n+1)/2; layer++) {
        for(int m = layer; m<n-layer; m++) res[layer][m]=num++;
        for(int m = layer+1; m<n-layer-1; m++) res[m][n-1-layer]=num++;
        for(int m =n-layer-1;m>layer; m--) res[n-1-layer][m]=num++;
        for(int m =n-layer-1;m>layer; m--) res[m][layer]=num++;
    }
    return res
}
```

## 62 & 63 Unique Paths

#### 原题链接
[https://leetcode.com/problems/unique-paths/description/](https://leetcode.com/problems/unique-paths/description/)
[https://leetcode.com/problems/unique-paths-ii/description/](https://leetcode.com/problems/unique-paths-ii/description/)

#### 题目
> A robot is located at the top-left corner of a _m_ x _n_ grid (marked 'Start' in the diagram below).
> The robot can only move either down or right at any point in time. The robot is trying to reach the bottom-right corner of the grid (marked 'Finish' in the diagram below).
> How many possible unique paths are there?
> **Note:** _m_ and _n_ will be at most 100.

> Follow up for "Unique Paths":
> Now consider if some obstacles are added to the grids. How many unique paths would there be?
> An obstacle and empty space is marked as `1` and `0` respectively in the grid.
> For example,
> There is one obstacle in the middle of a 3x3 grid as illustrated below.
> [
>   [0,0,0],
>   [0,1,0],
>   [0,0,0]
> ]
> The total number of unique paths is `2`.
> **Note:** _m_ and _n_ will be at most 100.

#### 思路

- 杨辉三角

- $C_m^n = \frac{m!}{n! (m-n)!}$ 不用`BigInteger`类的方法：
```java
for (int i = 1; i <= n; i++)
	ans = ans * (m - n + i) / i;
return (int) ans;
```
- 动态规划

#### 代码
```java
public int uniquePathsWithObstacles(int[][] obstacleGrid) { 
	if(obstacleGrid == null||obstacleGrid.length == 0 ) return 0;
	if(obstacleGrid[0].length == 0) return 1;
	int m = obstacleGrid.length;
	int n = obstacleGrid[0].length;
	int[][] dp = new int[m+1][n+1];
	dp[0][1] = 1;
	for(int i = 1; i <= m; i++)
		for(int j = 1; j <= n; j++)
			dp[i][j] = (obstacleGrid[i-1][j-1] == 0) ? dp[i-1][j] + dp[i][j-1] : 0;
	return dp[m][n];
}
```

## 209. Minimum Size Subarray Sum

#### 原题链接
[https://leetcode.com/problems/minimum-size-subarray-sum/description/](https://leetcode.com/problems/minimum-size-subarray-sum/description/)

#### 题目
> Given an array of **n** positive integers and a positive integer **s**, find the minimal length of a **contiguous** subarray of which the **sum ≥ s**. If there isn't one, return 0 instead.
> For example, given the array `[2,3,1,2,4,3]` and `s = 7`,
> the subarray `[4,3]` has the minimal length under the problem constraint.

#### 思路
- 注意审题，是**sum ≥ s**
- 答案的代码更简洁
	- `sum == s`的情况应该和`sum > s`一起考虑而不是和`sum < s`一起考虑

#### 代码
```java
public int minSubArrayLen(int s, int[] nums) {
    if (nums == null || nums.length == 0) return 0;
    int i = 0, j = 0, sum = 0, min = Integer.MAX_VALUE;
    while (j < nums.length) {
        sum += nums[j++];
        while (sum >= s) {
          min = Math.min(min, j - i);
          sum -= nums[i++];
        }
    }
    return min == Integer.MAX_VALUE ? 0 : min;
}
```


## 78. Subsets

#### 原题链接
[https://leetcode.com/problems/subsets/description/](https://leetcode.com/problems/subsets/description/)

#### 题目
> Given a set of **distinct** integers, _nums_, return all possible subsets (the power set).
> **Note:** The solution set must not contain duplicate subsets.
> For example,
> If **_nums_** = `[1,2,3]`, a solution is:
> [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]

#### 思路
- 每添加一个新数其实就是在原有的子集中的每一个集合后面都加上这个数

#### 代码
```java
public List<List<Integer>> subsets(int[] nums) {

        List<List<Integer>> sub = new ArrayList<List<Integer>>();

        sub.add(new ArrayList<Integer>());

        for (int i = 0; i < nums.length; i++) {

            int curLen = sub.size();

            for (int j = 0; j < curLen; j++) {

                List<Integer> tmp = new ArrayList<Integer>(sub.get(j));

                tmp.add(nums[i]);

                sub.add(tmp);

            }

        }

        return sub;

    }
```

## 162. Find Peak Element
	
#### 原题链接
[https://leetcode.com/problems/find-peak-element/description/](https://leetcode.com/problems/find-peak-element/description/)

#### 题目
> A peak element is an element that is greater than its neighbors.
> Given an input array where `num[i] ≠ num[i+1]`, find a peak element and return its index.
> The array may contain multiple peaks, in that case return the index to any one of the peaks is fine.
> You may imagine that `num[-1] = num[n] = -∞`.
> For example, in array `[1, 2, 3, 1]`, 3 is a peak element and your function should return the index number 2.
> **Note:**
> **Your solution should be in logarithmic complexity.**

#### 思路
- 注意！本题有一个要点就是`num[-1] = num[n] = -∞`，因此可以用二分法
- 二分法原理
	- $mid  = (lo + hi) / 2$
	- 哪边鼓起来就去哪边找
	- 如果都不鼓起来就返回好啦

#### 代码
```java
public int findPeakElement(int[] nums) {
    if (nums.length == 0) return nums[0];
    int lo = 0, hi = nums.length-1;
    while (hi - lo > 1) {
        int mid = (lo + hi) / 2;
        if (nums[mid] < nums[mid-1]) hi = mid;
        else if (nums[mid] < nums[mid+1]) lo = mid;
        else return mid;
    }
    if (nums[lo] < nums[hi]) return hi;
    else return lo;
}
```



[^_^]:
	## 模板
	
	#### 原题链接
	[]()
	
	#### 题目
	
	
	#### 思路
	
	
	#### 代码
	```java

	```
