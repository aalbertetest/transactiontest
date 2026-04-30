/**
 * Reverses a string using split/reverse/join.
 * @param {string} str
 * @returns {string}
 */
function reverseString(str) {
  return str.split("").reverse().join("");
}

/**
 * Reverses a string by iterating from the end to the start.
 * @param {string} str
 * @returns {string}
 */
function reverseStringAlt(str) {
  let reversed = "";
  for (let i = str.length - 1; i >= 0; i--) {
    reversed += str[i];
  }
  return reversed;
}

module.exports = { reverseString, reverseStringAlt };
