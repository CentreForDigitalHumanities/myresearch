# Overview of Permissions in MyResearch

This document was last edited on 02-10-2025. May need to be updated!

For the MVP of MyResearch, Permissions will look something like this:

| MyResearch Portal Permissions MVP   | User (authenticated)   | User (not authenticated)   | Chamber members   | Privacy Officer   |
|:------------------------------------|:-----------------------|:---------------------------|:------------------|:------------------|
| 1. Studies (draft)                  |                        |                            |                   |                   |
| 1.1 Lists                           | Access to own          | No access                  | Access to own     | Access to own     |
| 1.2 Application detail              | Access to own          | No access                  | Access to own     | Access to own     |
| 1.2 Create                          | Access to own          | No access                  | Access to own     | Access to own     |
| 1.3 Update                          | Access to own          | No access                  | Access to own     | Access to own     |
| 1.4 Delete                          | Access to own          | No access                  | Access to own     | Access to own     |
|                                     |                        |                            |                   |                   |
| 2 Studies (submitted)               |                        |                            |                   |                   |
| 2.1 Lists                           | Access to own          | No access                  | Access            | Access            |
| 2.2 Detail page                     | Access to own          | No access                  | Access            | Access            |
| 2.3 View PDF                        | Access to own          | No access                  | Access            | Access            |
|                                     |                        |                            |                   |                   |
| 3 Processing registry reviews       |                        |                            |                   |                   |
| 3.1 Submit decision                 | No access              | No access                  | No access         | Access            |
| 3.1 Close review                    | No access              | No access                  | No access         | Access            |
|                                     |                        |                            |                   |                   |
| 4 Roadmap                           |                        |                            |                   |                   |
| 4.1 Questionaire                    | Access                 | Access (not saved)         | Access            | Access            |

# Possible future permissions in MyResearch

Once the FETC Portal gets incorporated, we can expect the permissions to become something like the table below.

These permissions are based on the currently-in-production FETC Portal. Ideally, we can streamline and simplify the FETC Portal's functionality when we incorporate it into MyResearch.

| MyResearch Portal Permissions   | User (logged-in)             | User (not authenticated)   | Chamber members   | Privacy Officer      | Data manager         | Chair                | Secretary     |
|:--------------------------------|:-----------------------------|:---------------------------|:------------------|:---------------------|:---------------------|:---------------------|:--------------|
| 1. Studies (draft)              |                              |                            |                   |                      |                      |                      |               |
| 1.1 Lists                       | Access to own                | No access                  | Access to own     | Access to own        | Access to own        | Access to own        | Access to own |
| 1.2 Application detail          | Access to own                | No access                  | Access to own     | Access to own        | Access to own        | Access to own        | Access to own |
| 1.2 Create                      | Access to own                | No access                  | Access to own     | Access to own        | Access to own        | Access to own        | Access to own |
| 1.3 Update                      | Access to own                | No access                  | Access to own     | Access to own        | Access to own        | Access to own        | Access to own |
| 1.4 Delete                      | Access to own                | No access                  | Access to own     | Access to own        | Access to own        | Access to own        | Access to own |
|                                 |                              |                            |                   |                      |                      |                      |               |
| 2 Studies (submitted)           |                              |                            |                   |                      |                      |                      |               |
| 2.1 Lists                       | Access to own                | No access                  | Access            | Access               | Unknown              | Unknown              | Unknown       |
| 2.2 Detail page                 | Access to own                | No access                  | Access            | Access               | Unknown              | Unknown              | Unknown       |
| 2.3 View PDF                    | Access to own                | No access                  | Access            | Access               | Unknown              | Unknown              | Unknown       |
|                                 |                              |                            |                   |                      |                      |                      |               |
| 3 Processing registry reviews   |                              |                            |                   |                      |                      |                      |               |
| 3.1 Submit decision             | No access                    | No access                  | No access         | Access               | No Access            | No Access            | No Access     |
| 3.1 Close review                | No access                    | No access                  | No access         | Access               | No Access            | No Access            | No Access     |
|                                 |                              |                            |                   |                      |                      |                      |               |
| 4 Archives                      |                              |                            |                   |                      |                      |                      |               |
| 4.1 Public archive              | Access                       | Access                     | Access            | Access               | Access               | Access               | Access        |
| 4.2 User archive                | Access if user is Humanities | No access                  | Access            | Access               | Access               | Access               | Access        |
| 4.3 Site-export                 | No access                    | No access                  | Access            | No access            | No access            | No access            | Access        |
|                                 |                              |                            |                   |                      |                      |                      |               |
| 5 Fetc reviews                  |                              |                            |                   |                      |                      |                      |               |
| 5.1 Submit decision             | No access                    | No access                  | Access to own     | Access to own        | Access to own        | Access to own        | Access to own |
| 5.2 Close review                | No access                    | No access                  | No access         | No access            | No access            | No access            | Access        |
| 5.3 Discontinue review          | No access                    | No access                  | No access         | No access            | No access            | No access            | Access        |
| 5.4 Update documents            | No access                    | No access                  | No access         | No access            | No access            | No access            | Access        |
| 5.5 Workload overview           | No access                    | No access                  | No access         | No access            | No access            | Access               | Access        |
| 5.6 Change Chamber              | No access                    | No access                  | No access         | No access            | No access            | No access            | Access        |
| 5.7 Assign reviewers            | No access                    | No access                  | No access         | No access            | No access            | No access            | Access        |
|                                 |                              |                            |                   |                      |                      |                      |               |
| 6 Roadmap                       |                              |                            |                   |                      |                      |                      |               |
| 6.1 Questionaire                | Access                       | Access                     | Access            | Access               | Access               | Access               | Access        |