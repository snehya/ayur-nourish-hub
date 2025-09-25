import { useEffect, useState } from 'react';

/**
 * Custom hook for parallax scrolling effects
 */
export const useParallax = () => {
  const [scrollY, setScrollY] = useState(0);

  useEffect(() => {
    const handleScroll = () => setScrollY(window.scrollY);
    
    window.addEventListener('scroll', handleScroll, { passive: true });
    
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return scrollY;
};

/**
 * Custom hook for element visibility in viewport
 */
export const useInView = (threshold = 0.1) => {
  const [isInView, setIsInView] = useState(false);
  const [element, setElement] = useState<HTMLElement | null>(null);

  useEffect(() => {
    if (!element) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        setIsInView(entry.isIntersecting);
      },
      { threshold }
    );

    observer.observe(element);

    return () => observer.disconnect();
  }, [element, threshold]);

  return [setElement, isInView] as const;
};

/**
 * Get parallax transform value based on scroll position
 */
export const getParallaxTransform = (scrollY: number, speed = 0.5) => {
  return `translateY(${scrollY * speed}px)`;
};

/**
 * Get scale transform value based on scroll position
 */
export const getScaleTransform = (scrollY: number, speed = 0.0001, min = 1, max = 1.2) => {
  const scale = Math.min(max, Math.max(min, 1 + scrollY * speed));
  return `scale(${scale})`;
};

/**
 * Get opacity value based on scroll position
 */
export const getOpacityValue = (scrollY: number, start = 0, end = 300) => {
  if (scrollY <= start) return 1;
  if (scrollY >= end) return 0;
  return 1 - (scrollY - start) / (end - start);
};