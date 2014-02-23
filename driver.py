#!/usr/bin/python
import csv, random
from pprint import pprint
from collections import defaultdict

def main():

  ### adjust settings here ###

  # set number of graders per problem.
  # graders will be evenly distributed across problems whose value is 0.
  problems = {
    '1-1': 2,
    '1-2': 2,
    '1-3': 5,
    '1-4': 0,
    '1-5': 0,
    '1-6': 0,
  }

  ### create assignments ###

  # get lists of graders and students by username
  students = map(str.strip, open('students.txt').readlines())
  graders = map(str.strip, open('graders.txt').readlines())

  # determine number of free graders and problems
  free_problems =\
    [prob for (prob, num_graders) in problems.iteritems() if num_graders == 0]
  num_free_problems = len(free_problems)
  num_free_graders = len(graders) - sum(problems.values())

  # evenly distribute free graders over free problems
  floor_num_per_free_problem = num_free_graders // num_free_problems
  for free_problem in free_problems:
    problems[free_problem] = floor_num_per_free_problem

  # probably not perfectly divisible, so randomly add in stragglers
  num_leftover_graders = num_free_graders % num_free_problems
  for free_problem in random.sample(free_problems, num_leftover_graders):
    problems[free_problem] += 1

  # assign specific graders to problems
  assignments = {}
  graders_queue = graders[:] # avoid modifying original graders list
  random.shuffle(graders_queue)
  for (problem, num_graders) in problems.iteritems():
    bounds = [i * len(students) / num_graders for i in xrange(num_graders)]
    bounds.append(len(students))
    student_partitions =\
      [students[bounds[i]:bounds[i+1]] for i in xrange(len(bounds) - 1)]
    for partition in student_partitions:
      grader = graders_queue.pop()
      assignments[grader] = (problem, partition)

  ### print summary of assignments ###
  print "Grader Assignments"
  pprint({grader: (problem, len(students))\
    for (grader, (problem, students)) in assignments.iteritems()})

  ### verify assignment integrity ###
  assert set(assignments.keys()) == set(graders),\
    "not all graders were assigned"
  for problem in problems:
    students_for_problem = []
    for grader, (prob_i, student_partition) in assignments.iteritems():
      if prob_i == problem:
        students_for_problem.extend(student_partition)
    assert set(students_for_problem) == set(students),\
      "not all students were partitioned for problem %s" % (problem, )
    assert len(set(students_for_problem)) == len(students_for_problem),\
      "students were redundantly assigned for problem %s" % (problem, )

  ### create csv files ###
  for (grader, (problem, students)) in assignments.iteritems():
    file_name = "%s.csv" % (grader, )
    with open(file_name, 'wb') as csvfile:
      writer = csv.writer(csvfile)
      writer.writerow(["problem", "student", "grade", "comment"])
      for student in students:
        quoted_problem_str = '"%s"' % (problem, )
        writer.writerow([quoted_problem_str, student, None, None])

if __name__ == '__main__':
  main()
