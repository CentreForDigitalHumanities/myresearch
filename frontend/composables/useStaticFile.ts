export default function (path: string) {
    const runtimeConfig = useRuntimeConfig();

    return `${runtimeConfig.public.static_dir}${path}`;
}
