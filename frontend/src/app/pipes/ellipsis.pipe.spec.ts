import { EllipsisPipe } from './ellipsis.pipe';

describe('EllipsisPipe', () => {
  it('create an instance', () => {
    const pipe = new EllipsisPipe();
    expect(pipe).toBeTruthy();
  });

  it('should return the same value if limit is not provided', () => {
    const pipe = new EllipsisPipe();
    expect(pipe.transform('test')).toEqual('test');
  });

  it('should return shorter value with ellipsis if longer than limit', () => {
    const pipe = new EllipsisPipe();
    expect(pipe.transform('long text', 6)).toEqual('long t...');
  });
});
