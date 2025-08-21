import { i18n } from "~/plugins/i18n";

type TranslateableObject<Key extends string> = {
    [K in `${Key}Nl` | `${Key}En`]?: string | null;
};

function useTranslateableAttribute<Key extends string>(
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

export { useTranslateableAttribute };
