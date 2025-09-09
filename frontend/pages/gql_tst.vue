<script lang="ts" setup>
import { BSButton } from "cdh-vue-lib";
import { graphql } from "~/generated/gql";
import { useQuery, useMutation } from "@vue/apollo-composable";
import { type GetAllUsersQuery, type CreateUser } from "~/generated/gql/graphql";

// WARNING!
// THIS IS A PROOF-OF-CONCEPT FOR GRAPHQL!
// REMOVE THIS PAGE AND QUERY ONCE WE HAVE ACTUAL CONTENT!

const GET_USERS = graphql(`
    query getAllUsers {
        users {
            id
            username
            email
        }
    }
`);

const CREATE_USER = graphql(`
  mutation CreateUser($email: String!, $username: String!) {
    createUser(email: $email, username: $username) {
      user {
        email
        id
        username
      }
    }
}`
)

const {
  result: usersResult,
  loading: usersLoading,
  error: usersError,
  refetch,
} = useQuery<GetAllUsersQuery>(GET_USERS);


const username = ref("");
const email = ref("");

const { mutate: createUser, loading: createUserLoading, error: createUserError } = useMutation<CreateUser>(CREATE_USER);

function submitUser() {
  createUser({
    email: email.value,
    username: username.value,
  }).then(() => {
    refetch();
    username.value = "";
    email.value = "";
  });
}

</script>

<template>
  <h3 class="mt-3">Scroll to the bottom to add a new user!</h3>
  <div>
    <p v-for="user in usersResult?.users ?? []" :key="user.id">
      {{ user.username }} {{ user.email }}
    </p>
  </div>
          <div class="col-12 col-lg-10">
            <form class="uu-form" @submit.prevent="submitUser">
                  <div class="uu-form-row">
    <div class="d-flex flex-column">
    <div class="uu-form-field">
      <label class="form-label">
        Add User:
      </label>
      <p
          class="text-muted"
      >
          You can add another user here!
      </p>
      <p>
          Username:
      </p>
      <input
          v-model="username"
          type="text"
          class="form-control"
      />
      <p>
          E-mail:
      </p>
      <input
          v-model="email"
          type="text"
          class="form-control"
      />
      </div>
    </div>
  </div>
  <div class="btn-group mb-2">
      <BSButton
          variant="primary"
          type="submit"
          :loading="createUserLoading"
      >
          {{ $t("Submit") }}
      </BSButton>
  </div>
            </form>
        </div>
</template>
