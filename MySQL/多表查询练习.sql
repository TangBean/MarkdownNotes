/* 1. 查出至少有一个员工的部门。显示部门编号、部门名称、部门位置、部门人数。*/
SELECT z.deptno 部门编号, d.dname 部门名称, d.loc 部门位置, z.cnt 部门人数
FROM (SELECT deptno, COUNT(*) cnt FROM emp GROUP BY deptno HAVING COUNT(*) >= 1) z, dept d
WHERE z.deptno=d.deptno

/* 2. 列出薪金比关羽高的所有员工。*/
SELECT * 
FROM emp e
WHERE e.sal > (SELECT sal FROM emp WHERE ename='关羽')

/* 3. 列出所有员工的姓名及其直接上级的姓名。*/
SELECT e.ename 员工姓名, IFNULL(m.ename, '老板') 上级姓名
FROM emp e LEFT OUTER JOIN emp m
ON e.mgr=m.empno

/* 4. 列出受雇日期早于直接上级的所有员工的编号、姓名、部门名称。*/
SELECT e.empno 员工编号, e.ename 姓名, d.dname 部门名称
FROM emp e LEFT OUTER JOIN emp m
ON e.mgr=m.empno
LEFT OUTER JOIN dept d
ON e.deptno=d.deptno
WHERE e.hiredate>m.hiredate

/* 5. 列出部门名称和这些部门的员工信息，同时列出那些没有员工的部门。*/
/* 因为以部门为主，所以是 RIGHT OUTER JOIN */
SELECT e.*, d.dname
FROM emp e RIGHT OUTER JOIN dept d
ON e.deptno=d.deptno;

/* 6. 列出所有文员的姓名及其部门名称，部门的人数。*/
SELECT e.ename 姓名, d.dname 部门名称,  z.cnt 部门人数
FROM emp e, dept d, (SELECT deptno, COUNT(*) cnt FROM emp GROUP BY deptno) z
WHERE e.job='文员' AND e.deptno=d.deptno AND z.deptno=e.deptno

/* 7. 列出最低薪金大于15000的各种工作及从事此工作的员工人数。*/
SELECT job, COUNT(*)
FROM emp
GROUP BY job
HAVING MIN(sal) > 15000

/* 8. 列出在销售部工作的员工的姓名，假定不知道销售部的部门编号。*/
SELECT ename
FROM emp
WHERE deptno=(SELECT deptno FROM dept WHERE dname='销售部')

/* 9. 列出薪金高于公司平均薪金的所有员工信息，所在部门名称，上级领导，工资等级。*/
SELECT e.*, d.dname '部门名称', m.ename '上级领导', g.grade '工资等级'
FROM emp e 
LEFT OUTER JOIN dept d ON e.deptno=d.deptno
LEFT OUTER JOIN emp m ON e.mgr=m.empno
LEFT OUTER JOIN salgrade g ON e.sal BETWEEN g.losal AND g.hisal
WHERE e.sal > (SELECT AVG(sal) FROM emp)

/* 10.列出与庞统从事相同工作的所有员工及部门名称。*/
SELECT e.*, d.dname
FROM emp e, dept d
WHERE e.job=(SELECT job FROM emp WHERE ename='庞统') AND e.deptno=d.deptno AND e.ename != '庞统'

/* 11.列出薪金高于在部门30工作的所有员工的薪金的员工姓名和薪金、部门名称。*/
SELECT e.ename, e.sal, d.dname
FROM emp e, dept d
WHERE e.sal > ALL (SELECT sal FROM emp WHERE deptno=30) AND e.deptno=d.deptno

/* 12.列出每个部门的员工数量、平均工资。*/
SELECT d.dname '部门', c.cnt '员工数量', c.avg_sal '平均工资'
FROM dept d, (SELECT deptno, COUNT(*) cnt, AVG(sal) avg_sal FROM emp GROUP BY deptno) c
WHERE d.deptno=c.deptno

