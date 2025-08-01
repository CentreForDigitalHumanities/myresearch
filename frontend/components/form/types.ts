import type { SideBarConfig } from "../shared/FormSideBar.vue";

interface BaseFormElement {
  labelNl?: string;
  labelEn?: string;
  descriptionNl?: string;
  descriptionEn?: string;
}

interface Orderable {
  order: number;
}
export interface FormConfig extends BaseFormElement {
  steps: FormStep[];
}
export interface FormStep extends BaseFormElement, Orderable {
  slug: string;
  stepNameNL: string;
  stepNameEN: string;
  questions: Question[];
  substeps?: FormStep[];
  sideConfig?: SideBarConfig;
}

interface BaseQuestion extends BaseFormElement, Orderable {
  id: string;
  required?: boolean;
  disabled?: boolean;
}

export interface TextQuestion extends BaseQuestion {
  type: "text";
  placeholderNl?: string;
  placeholderEn?: string;
  lines?: number; // For multiline text / textarea questions.
}

interface MultipleTextQuestion extends TextQuestion {
  multiple: true;
  buttonTextNl: string;
  buttonTextEn: string;
}

interface SelectOption {
  value: string;
  labelNl: string;
  labelEn: string;
}

export interface SelectQuestion extends BaseQuestion {
  type: "select";
  options: SelectOption[];
}
export interface DateQuestion extends BaseQuestion {
  type: "date";
}

interface CheckboxQuestion extends BaseQuestion {
  type: "checkbox";
  options: SelectOption[];
}

type Question =
  | TextQuestion
  | MultipleTextQuestion
  | SelectQuestion
  | DateQuestion
  | CheckboxQuestion;
