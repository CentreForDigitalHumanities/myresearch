import type { OperationVariables } from "@apollo/client";
import type { UUListTypes } from "cdh-vue-lib";

export interface GraphQLListVariables extends OperationVariables {
  limit?: number | null;
  offset?: number | null;
  search?: string | null;
  ordering?: string | null;
}

export type GraphQLListData<Item extends UUListTypes.Data<string>> = {
  pageInfo: {
    count?: number | null;
    offset?: number | null;
    limit?: number | null;
  };
  results: (Item | null)[];
};
