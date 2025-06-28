export function sanitizeInput(str: string): string {
  // 간단한 XSS 방어: 태그 제거
  return str.replace(/<[^>]*>?/gm, '');
}
