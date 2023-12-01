import { DefaultIfEmptyPipe } from './default-if-empty.pipe';

describe('DefaultIfEmptyPipe', () => {
  it('create an instance', () => {
    const pipe = new DefaultIfEmptyPipe();
    expect(pipe).toBeTruthy();
  });
});
