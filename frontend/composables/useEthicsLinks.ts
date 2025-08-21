import { i18n } from "~/plugins/i18n";

/*
 * @param [tag] accepted tags: FEtC_H, FEtC_H_regulations, model_documents
 */
export default function useEthicsLinks(tag: string): string {
  const { locale } = i18n.global;

  for (let i = 0; i < ethicsLinks.length; i++) {
    if (ethicsLinks[i].tag === tag) {
      if (locale === "nl") {
        return ethicsLinks[i].nl;
      }
      return ethicsLinks[i].en;
    }
  }
  return "";
}

const ethicsLinks = [
  {
    tag: "FEtC_H",
    nl: "https://fetc-gw.wp.hum.uu.nl/",
    en: "https://fetc-gw.wp.hum.uu.nl/en/",
  },
  {
    tag: "FEtC_H_regulations",
    nl: "https://fetc-gw.wp.hum.uu.nl/reglement-fetc-gw/",
    en: "https://fetc-gw.wp.hum.uu.nl/en/regulations-fetc-h/",
  },
  {
    tag: "model_documents",
    nl: "https://intranet.uu.nl/documenten-ethische-toetsingscommissie-gw",
    en: "https://intranet.uu.nl/en/documents-ethics-assessment-committee-humanities",
  },
];
