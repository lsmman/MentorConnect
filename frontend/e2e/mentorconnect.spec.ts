import { test, expect } from '@playwright/test';

const BASE_URL = 'http://localhost:3000';
const TEST_EMAIL = 'testuser_e2e@example.com';
const TEST_PASSWORD = 'testpass123';

// 실제 백엔드가 초기화된 상태에서 실행해야 하며, DB는 테스트 계정이 중복되지 않도록 관리 필요

test.describe('MentorConnect E2E', () => {
  test('회원가입 → 로그인 → 멘토 목록 → 매칭 요청', async ({ page }) => {
    // 회원가입
    await page.goto(`${BASE_URL}/signup`);
    await page.fill('input[name="name"]', '테스트유저');
    await page.fill('input[name="email"]', TEST_EMAIL);
    await page.fill('input[name="password"]', TEST_PASSWORD);
    await page.selectOption('select[name="role"]', 'mentee');
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL(/login/);

    // 로그인
    await page.goto(`${BASE_URL}/login`);
    await page.fill('input[name="email"]', TEST_EMAIL);
    await page.fill('input[name="password"]', TEST_PASSWORD);
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL(/mentors/);

    // 멘토 목록 조회
    await expect(page.locator('.mentor-list')).toBeVisible();
    const mentorCount = await page.locator('.mentor-card').count();
    expect(mentorCount).toBeGreaterThan(0);

    // 매칭 요청 (첫 번째 멘토)
    const firstMentorRequestBtn = page.locator('.mentor-card button:has-text("매칭 요청")').first();
    if (await firstMentorRequestBtn.isVisible()) {
      await firstMentorRequestBtn.click();
      await expect(page.locator('.toast-success, .alert-success')).toHaveText(/요청 완료|성공|sent/i);
    }
  });
});
