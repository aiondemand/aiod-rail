import { FormatPlatformNamePipe } from './format-platform-name.pipe';

describe('FormatPlatformNamePipe', () => {
  it('create an instance', () => {
    const pipe = new FormatPlatformNamePipe();
    expect(pipe).toBeTruthy();
  });

  it('should format huggingface as HuggingFace', () => {
    const pipe = new FormatPlatformNamePipe();
    expect(pipe.transform('huggingface')).toBe('HuggingFace');
  });

  it('should format HUGGINGFACE as HuggingFace', () => {
    const pipe = new FormatPlatformNamePipe();
    expect(pipe.transform('HUGGINGFACE')).toBe('HuggingFace');
  });

  it('should format " HuGGingFace" as HuggingFace', () => {
    const pipe = new FormatPlatformNamePipe();
    expect(pipe.transform('HuGGingFace')).toBe('HuggingFace');
  });
});
