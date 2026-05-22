import { SubmissionStatus } from "~/generated/gql/graphql";
import { i18n } from "~/plugins/i18n";

const { t } = i18n.global;

const STATUS_TRANSLATIONS: Record<SubmissionStatus, string> = {
    [SubmissionStatus.Approved]: t("Approved"),
    [SubmissionStatus.Draft]: t("Draft"),
    [SubmissionStatus.Rejected]: t("Rejected"),
    [SubmissionStatus.Submitted]: t("Submitted"),
};

export function useTranslatedStatus(status: SubmissionStatus): string {
    return STATUS_TRANSLATIONS[status];
}
