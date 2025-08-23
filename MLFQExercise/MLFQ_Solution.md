# MLFQ — Operating System

**Prepared by:** _Virak Rith_

---

## Solution

### 1) Constructing Gantt Chart

**Queue Configuration**

- **Q0:** Round Robin, Time Quantum = 2
- **Q1:** Round Robin, Time Quantum = 4
- **Q2:** FCFS

**Per-queue timeline**

```
Q0:  P1   P2   P3   P4
     |----|----|----|----|
     0    2    4    6    8

                    Q1:  P1        P2   P3        P4
                         |--------| |--| |--------| |---|
                         8        12   14         18    21

                                                   Q2:  P1   P3
                                                        |-|  |---|
                                                        21   22  25
```

**Gantt Chart (merged view):**  
`| P1 | P2 | P3 | P4 | P1 | P2 | P3 | P4 | P1 | P3 |`  
`0    2    4    8    12   14   18   21   22   25`

---

### 2) Queue Transitions

- **P1:** Q0 → Q1 → Q2
- **P2:** Q0 → Q1
- **P3:** Q0 → Q1 → Q2
- **P4:** Q0 → Q1

---

### 3) Calculations

Let TAT = CT − Arrival Time, WT = TAT − Burst Time.

| Process | Arrival | Burst | Completion Time (CT) | Turnaround Time (TAT) | Waiting Time (WT) | Transitions  |
| :-----: | :-----: | :---: | :------------------: | :-------------------: | :---------------: | :----------- |
|   P1    |    0    |   7   |          22          |          22           |        15         | Q0 → Q1 → Q2 |
|   P2    |    1    |   4   |          14          |          13           |         9         | Q0 → Q1      |
|   P3    |    2    |   9   |          25          |          23           |        14         | Q0 → Q1 → Q2 |
|   P4    |    3    |   5   |          21          |          18           |        13         | Q0 → Q1      |

**Averages**

- Average TAT = (22 + 13 + 23 + 18) / 4 = **19.00**
- Average WT = (15 + 9 + 14 + 13) / 4 = **12.75**

---

### 4) Promotions (wait > 10 time units)

- **None** — no process waited more than 10 time units in Q1 or Q2, so no promotion was triggered.

---

## Link to GitHub Account : [Click Here](https://github.com/Poppykhim/OS_TP.git) <3
