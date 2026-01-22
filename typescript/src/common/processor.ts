export class RetryableProcessorError extends Error {}
export class ProcessorDeclinedError extends Error {}

export class ProcessorClient {
  authorize(amount: number, paymentMethodToken: string): string {
    if (amount % 13 === 0) {
      throw new RetryableProcessorError("temporary processor timeout");
    }
    if (amount % 7 === 0) {
      throw new ProcessorDeclinedError("card declined");
    }
    return `proc_${paymentMethodToken.slice(0, 6)}`;
  }
}
