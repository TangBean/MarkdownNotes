/* 1. 查询出部门编号为30的所有员工。*/
SELECT empno FROM emp WHERE deptno = 30;

/* 2. 所有销售员的姓名、编号和部门编号。*/
SELECT ename,empno,deptno FROM emp WHERE job = '销售员';

/* 3. 找出奖金高于工资的员工。*/
SELECT * FROM emp WHERE comm > sal;

/* 4. 找出奖金高于工资60%的员工。*/
SELECT * FROM emp WHERE comm > 0.6 * sal;

/* 5. 找出部门编号为10中所有经理，和部门编号为20中所有销售员的详细资料。*/
SELECT * FROM emp WHERE (deptno = 10 AND job = '经理') OR (deptno = 20 AND job = '销售员');

/* 6. 找出部门编号为10中所有经理，部门编号为20中所有销售员，还有即不是经理又不是销售员但其工资大或等于20000的所有员工详细资料。*/
SELECT * FROM emp WHERE (deptno = 10 AND job = '经理') OR (deptno = 20 AND job = '销售员') OR (job NOT IN ('经理', '销售员') AND sal >= 20000);

/* 8. 无奖金或奖金低于1000的员工。*/
SELECT ename FROM emp WHERE comm IS NULL OR comm < 1000;

/* 9. 查询名字由三个字组成的员工。*/
SELECT * FROM emp WHERE ename LIKE '___';

/* 10.查询2000年入职的员工。*/
SELECT * FROM emp WHERE hiredate LIKE '2000-%';

/* 11. 查询所有员工详细信息，用编号升序排序。*/
SELECT * FROM emp ORDER BY empno;

/* 12. 查询所有员工详细信息，用工资降序排序，如果工资相同使用入职日期升序排序。*/
SELECT * FROM emp ORDER BY sal DESC, hiredate;

/* 13. 查询每个部门的平均工资。*/
SELECT deptno, AVG(sal) 平均工资 FROM emp GROUP BY deptno;

/* 14. 查询每个部门的雇员数量。 */
SELECT deptno, COUNT(*) FROM emp GROUP BY deptno;

/* 15. 查询每种工作的最高工资、最低工资、人数。*/
SELECT job, MAX(sal), MIN(sal), COUNT(*) FROM emp GROUP BY job;
