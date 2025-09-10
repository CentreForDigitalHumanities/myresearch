import { i18n } from "~/plugins/i18n";

export default function useEthicsLinks(tag: LinkTag): string {
  const { locale } = i18n.global;

  if (locale === "nl") {
    return ethicsLinks[tag].nl;
  } else if (locale === "en") {
    return ethicsLinks[tag].en;
  } else {
    return "";
  }
}

type LinkTag = "FEtC_H" | "FEtC_H_regulations" | "model_documents";

const ethicsLinks: Record<LinkTag, { nl: string; en: string }> = {
  FEtC_H: {
    nl: "https://fetc-gw.wp.hum.uu.nl/",
    en: "https://fetc-gw.wp.hum.uu.nl/en/",
  },
  FEtC_H_regulations: {
    nl: "https://fetc-gw.wp.hum.uu.nl/reglement-fetc-gw/",
    en: "https://fetc-gw.wp.hum.uu.nl/en/regulations-fetc-h/",
  },
  model_documents: {
    nl: "https://intranet.uu.nl/documenten-ethische-toetsingscommissie-gw",
    en: "https://intranet.uu.nl/en/documents-ethics-assessment-committee-humanities",
  },
};
