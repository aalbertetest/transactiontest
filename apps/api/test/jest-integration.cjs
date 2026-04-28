module.exports = {
  moduleFileExtensions: ['js', 'json', 'ts'],
  rootDir: '..',
  testRegex: 'test/.*\\.integration-spec\\.ts$',
  transform: { '^.+\\.(t|j)s$': ['ts-jest', { tsconfig: 'tsconfig.json' }] },
  testEnvironment: 'node',
  moduleNameMapper: {
    '^@saas/shared$': '<rootDir>/../../packages/shared/src/index.ts',
  },
};
