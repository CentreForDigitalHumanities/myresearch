import { SubmissionStatus } from "~/generated/gql/graphql";
import { useI18n } from "vue-i18n";

export function useTranslatedStatus(status: SubmissionStatus): string {
    const { t } = useI18n();

    const statusTranslations: Record<SubmissionStatus, string> = {
        [SubmissionStatus.Approved]: t("Approved"),
        [SubmissionStatus.Draft]: t("Draft"),
        [SubmissionStatus.Rejected]: t("Rejected"),
        [SubmissionStatus.Submitted]: t("Submitted"),
    };

    return statusTranslations[status];
}
