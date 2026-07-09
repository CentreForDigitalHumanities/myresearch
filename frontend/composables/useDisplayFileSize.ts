export function useDisplayFileSize(bytes: number) {
    const BYTES_IN_KB = 1024;
    const BYTES_IN_MB = BYTES_IN_KB * 1024;

    if (bytes < BYTES_IN_KB) {
        return `${bytes.toString()} B`;
    } else if (bytes < BYTES_IN_MB) {
        return `${(bytes / BYTES_IN_KB).toFixed(2)} KB`;
    } else {
        return `${(bytes / BYTES_IN_MB).toFixed(2)} MB`;
    }
}
