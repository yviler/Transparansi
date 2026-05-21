# UX Flow of the different user types

## Entry

1. At load into route / the app will re route to the login
2. User can pick to login, create a user, login as guest (no account, observe, but cant touch data)
3. At login, everyone will get access to the Dashboard

## Dashboard

The dashboard simply shows all current projects running, with each project being shown in a container,
each container shows the Name, Description, Head of Project, Expected Budget, Current Expenses, Time elapsed since started, each container is clickable, to access the specific project (/Project/{project_id})

## Project Page

The project page shows the details of the project, with the top being a summarized view (name, head, etc) and below that being the specific tasks that the project has, and each task(parent_task) can have a subtask and bill, while a subtask can have a bill, a parent task is completed if all the subtasks and bills in it are all marked as complete (each task (parent or child), can be given an upload, namely a report to show the specific details of each, such as invoices, details, etc)

## As a guest/observer

The guest are able to fully see everything that goes on, see projects, download reports, however they cannot create, delete, edit anything

## As a staff

Staff are given access to specific projects, in each project they are tasked, they can create, edit, delete tasks, subtasks, bills (requires approval from supervisors), outside of the projects they are tasked with, they can access, but not edit

## As a supervior

Supervisors control projects, they are given access to projects by Admin, and they can enroll Staff to Projects, review and approve changes in the projects they control

## As an admin

Admins control users, create projects, allocate budget from system_wallet to specific projects, they can add money to the system_wallet (mimics budget allocation from central organization)
