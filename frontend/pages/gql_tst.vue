<script lang="ts" setup>
import { graphql } from "~/generated/gql";
import { useQuery } from "@vue/apollo-composable"
import { type GetAllUsersQuery } from "~/generated/gql/graphql";

// WARNING!
// THIS IS A PROOF-OF-CONCEPT FOR GRAPHQL!
// REMOVE THIS PAGE AND QUERY ONCE WE HAVE ACTUAL CONTENT!

const GET_USERS = graphql(`
query getAllUsers {
  users {
    username
    email
  }
}`
);
    
    const {
      result: usersResult,
      loading: usersLoading,
      error: usersError
    } = useQuery<GetAllUsersQuery>(GET_USERS);
    
  </script>

<template>
  <div>
    <p v-for="user in usersResult?.users ?? []">{{ user.username }} {{ user.email }}</p>
  </div>
</template>