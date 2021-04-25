# Database Design Document
This document outlines the design for the Learning Python database.

## Introduction
The Learn Python web application aims to help beginners get started with programming in Python. Several modules will be hosted on the app, which will cover the basics of the language. Users will be able to submit code for each activity, where they will be graded on the output of their code. This database provides an efficient data storage system for the insertion, retrieval, modification and reporting of the data that is generated by this web app. 

## Overview
The database will use `SQLite` as the backend technology. The advantages of sqlite3 are:
- Fast performance
    - `SQLite` is a lightweight and performant piece of software. 
- Portability
    - The database is stored as a single file compatible with all operation systems, 32- and 64-bit
- Reliability
    - Content is updated continuously and has less LOC than other DB solutions.
- Simplicity
    - For a simple web app such as Learn Python, the simplicity and ease of use  of `SQLite` makes it an appropriate choice. 

## Access
The database will primarily be access by a `Flask` frontend written in Python. Users will be able to register, login, submit answers and track their progress through the web app.  

## Tables
 |     Table name     | Description                                                                                                      |
|:------------------:|------------------------------------------------------------------------------------------------------------------|
| User               | A description of the user, including their registration details and usage statistics                             |
| Activity           | Content that can just be some information, or information with a question and its associated answer and solution |
| Module             | A group of activities that come under a general theme                                                            |
| UserActivity       | A UserActivity is a joining table between User and Activity                                                      |
| Submission         | A submission is user-generated content for a specific UserActivity                                               |
| ActivityDependency | A table that tracks which activities must be completed before a specific activity is unlocked                    |
| ModuleDependency   | A table that tracks which modules must be completed before a specific module unlocks                             |

## User
A user is someone that uses the site. 

- `UserID`
- `firstname`
- `lastname`
- `username`
- `password_hash`
- `total_submissions`
- `lines_of_code`
- `num_correct`
- `num_incorrect`

## Activity
An activity is information and maybe a question
- `ActivityID`
- `prompt`
- `answer`
- `solution`
- `question`

## Module
A module is a group of related activities.
- `ModuleID`
- `Title`
- `Description`

## UserActivity
A UserActivity is the data associated with one User completing one Activity
- `UserActivityID`
- `UserID`
- `ActivityId`
- `count_submitted`
- `is_completed`

## Submission
A Submission is the data associated with a user submitting a solution to a UserActivity
- `SubmissionID`
- `Code`
- `Timestamp`

## ActivityDependency
An ActivityDependency is the relationship between one Activity and another which must be completed before the former can be accessed.
- `ActivityDependencyId`
- `parent`
- `child`

## ModuleDependency
A ModuleDependency is the relationship between one Module and another which must be completed before the former can be accessed.
- `ModuleDependencyId`
- `parent`
- `child`