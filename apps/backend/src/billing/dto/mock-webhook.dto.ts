import { IsObject, IsString } from 'class-validator';

export class MockWebhookDto {
  @IsString()
  type!: string;

  @IsObject()
  data!: Record<string, unknown>;
}
