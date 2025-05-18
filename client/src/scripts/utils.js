function createRegexFromMask(mask) {
    const regexString = mask
        .replace(/N/g, '[0-9]')          // N – цифра от 0 до 9
        .replace(/A/g, '[A-Z]')          // A – прописная буква латинского алфавита
        .replace(/a/g, '[a-z]')          // a – строчная буква латинского алфавита
        .replace(/X/g, '[A-Z0-9]')       // X – прописная буква латинского алфавита либо цифра от 0 до 9
        .replace(/Z/g, '[-_@]');          // Z – символ из списка: “-“, “_”, “@”

    return new RegExp(`^${regexString}$`);
}

export function filterInvalidSerialNumbers(serialNumbers, mask) {
    const regex = createRegexFromMask(mask);
    return serialNumbers.filter(serial => !regex.test(serial));
}

export function isValidSerialNumber(serialNumber, mask) {
    const regex = createRegexFromMask(mask);
    return regex.test(serialNumber);
}