import type { GetFormQuery } from "~/generated/gql/graphql";

export type QueriedForm = NonNullable<GetFormQuery["form"]>;
export type Step = NonNullable<QueriedForm["steps"][number]>;
export type Substep = NonNullable<Step["substeps"][number]>;

export type CombinedStep = Step | Substep;
