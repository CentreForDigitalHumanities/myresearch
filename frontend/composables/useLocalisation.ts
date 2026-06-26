import { i18n } from "~/plugins/i18n";

type TranslateableObject<Key extends string> = {
    [K in `${Key}Nl` | `${Key}En`]?: string | null;
};

export function useTranslateableAttribute<Key extends string>(
    modelObject: TranslateableObject<Key>,
    key: Key,
): string {
    const currentLocale = i18n.global.locale;
    const keyNl = `${key}Nl` as keyof TranslateableObject<Key>;
    const keyEn = `${key}En` as keyof TranslateableObject<Key>;

    // eslint-disable-next-line @typescript-eslint/no-unnecessary-condition
    const selectedKey = currentLocale.value === "nl" ? keyNl : keyEn;
    const value = modelObject[selectedKey];

    return value ?? "";
}

const timeFormat: Intl.DateTimeFormatOptions = {
    month: "long",
    day: "numeric",
    year: "numeric",
    hour: "numeric",
    minute: "numeric",
};

/**
 * localizes the isoString (from for example UTC time) into local datetime and handles translation
 * @param isoString The local date time formatted, see https://en.wikipedia.org/wiki/ISO_8601 or our DB for examples.
 */
export function useLocalDateTime(isoString: string) {
    return new Date(isoString).toLocaleTimeString(
        i18n.global.locale.value,
        timeFormat,
    );
}
