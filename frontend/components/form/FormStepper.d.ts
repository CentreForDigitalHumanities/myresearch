export interface FormStep {
    slug: string;
    labelNl: string;
    labelEn: string;
    substeps: FormStep[];
    completed: boolean;
    active: boolean;
    disabled: boolean;
}
export interface FormStepperConfig {
    steps: FormStep[];
}
