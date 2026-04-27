import { HttpError } from "./errors.js";

export function requireParam(value: string | string[] | undefined, name: string): string {
  if (typeof value !== "string" || value.trim() === "") {
    throw new HttpError(400, `${name} is required`, "VALIDATION_ERROR");
  }

  return value;
}
