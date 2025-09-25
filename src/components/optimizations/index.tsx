/**
 * @fileoverview Optimized React component patterns and higher-order components
 * @author AyurDiet Pro Team
 * @version 1.0.0
 */

import React, { memo, Suspense, lazy, ComponentType, Component, ErrorInfo, ReactNode } from 'react';
import { Skeleton } from '@/components/ui/skeleton';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';
import { RefreshCw, AlertTriangle } from 'lucide-react';

/**
 * Error fallback component for error boundaries
 */
interface ErrorFallbackProps {
  error: Error;
  resetErrorBoundary: () => void;
}

const ErrorFallback: React.FC<ErrorFallbackProps> = ({ error, resetErrorBoundary }) => (
  <div className="p-6 text-center">
    <Alert variant="destructive" className="mb-4">
      <AlertTriangle className="h-4 w-4" />
      <AlertDescription>
        Something went wrong: {error.message}
      </AlertDescription>
    </Alert>
    <Button onClick={resetErrorBoundary} variant="outline">
      <RefreshCw className="w-4 h-4 mr-2" />
      Try Again
    </Button>
  </div>
);

/**
 * Custom Error Boundary implementation
 */
interface ErrorBoundaryState {
  hasError: boolean;
  error?: Error;
}

interface ErrorBoundaryProps {
  children: ReactNode;
  fallback?: ComponentType<ErrorFallbackProps>;
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
}

class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    this.props.onError?.(error, errorInfo);
    console.error('Error caught by boundary:', error, errorInfo);
  }

  resetErrorBoundary = () => {
    this.setState({ hasError: false, error: undefined });
  };

  render() {
    if (this.state.hasError && this.state.error) {
      const FallbackComponent = this.props.fallback || ErrorFallback;
      return (
        <FallbackComponent
          error={this.state.error}
          resetErrorBoundary={this.resetErrorBoundary}
        />
      );
    }

    return this.props.children;
  }
}

/**
 * Loading fallback component for Suspense
 */
const LoadingFallback: React.FC<{ className?: string }> = ({ className = "p-6" }) => (
  <div className={className}>
    <div className="space-y-4">
      <Skeleton className="h-8 w-1/3" />
      <Skeleton className="h-4 w-full" />
      <Skeleton className="h-4 w-2/3" />
      <Skeleton className="h-32 w-full" />
    </div>
  </div>
);

/**
 * Higher-order component that adds error boundary and suspense handling
 * @param WrappedComponent - Component to wrap
 * @param options - Configuration options
 * @returns Enhanced component with error handling and loading states
 */
export function withErrorBoundary<P extends Record<string, any>>(
  WrappedComponent: ComponentType<P>,
  options: {
    fallback?: ComponentType<ErrorFallbackProps>;
    onError?: (error: Error, errorInfo: ErrorInfo) => void;
  } = {}
) {
  const { fallback, onError } = options;

  const EnhancedComponent = memo((props: P) => (
    <ErrorBoundary fallback={fallback} onError={onError}>
      <WrappedComponent {...props} />
    </ErrorBoundary>
  ));

  EnhancedComponent.displayName = `withErrorBoundary(${WrappedComponent.displayName || WrappedComponent.name})`;

  return EnhancedComponent;
}

/**
 * Higher-order component that adds lazy loading with suspense
 * @param importFn - Dynamic import function
 * @param options - Configuration options
 * @returns Lazy-loaded component with suspense handling
 */
export function withLazyLoading<P extends Record<string, any>>(
  importFn: () => Promise<{ default: ComponentType<P> }>,
  options: {
    fallback?: React.ReactNode;
    errorFallback?: ComponentType<ErrorFallbackProps>;
  } = {}
) {
  const { fallback = <LoadingFallback />, errorFallback } = options;
  
  const LazyComponent = lazy(importFn);
  
  const EnhancedComponent = memo((props: P) => (
    <ErrorBoundary fallback={errorFallback}>
      <Suspense fallback={fallback}>
        <LazyComponent {...(props as any)} />
      </Suspense>
    </ErrorBoundary>
  ));

  EnhancedComponent.displayName = `withLazyLoading(LazyComponent)`;

  return EnhancedComponent;
}

/**
 * Memoized list item component for better performance in large lists
 * @param props - List item props
 * @returns Memoized list item
 */
interface OptimizedListItemProps {
  id: string | number;
  children: React.ReactNode;
  className?: string;
  onClick?: (id: string | number) => void;
}

export const OptimizedListItem = memo<OptimizedListItemProps>(
  ({ id, children, className, onClick }) => {
    const handleClick = React.useCallback(() => {
      onClick?.(id);
    }, [id, onClick]);

    return (
      <div className={className} onClick={handleClick}>
        {children}
      </div>
    );
  },
  // Custom comparison function for better memoization
  (prevProps, nextProps) => {
    return (
      prevProps.id === nextProps.id &&
      prevProps.className === nextProps.className &&
      prevProps.onClick === nextProps.onClick &&
      React.isValidElement(prevProps.children) &&
      React.isValidElement(nextProps.children) &&
      prevProps.children.key === nextProps.children.key
    );
  }
);

OptimizedListItem.displayName = 'OptimizedListItem';

/**
 * Virtual scrolling component for large datasets
 */
interface VirtualScrollProps<T> {
  items: T[];
  itemHeight: number;
  containerHeight: number;
  renderItem: (item: T, index: number) => React.ReactNode;
  className?: string;
}

export function VirtualScroll<T>({
  items,
  itemHeight,
  containerHeight,
  renderItem,
  className = ""
}: VirtualScrollProps<T>) {
  const [scrollTop, setScrollTop] = React.useState(0);

  const visibleCount = Math.ceil(containerHeight / itemHeight);
  const startIndex = Math.floor(scrollTop / itemHeight);
  const endIndex = Math.min(startIndex + visibleCount + 1, items.length);

  const visibleItems = React.useMemo(
    () => items.slice(startIndex, endIndex),
    [items, startIndex, endIndex]
  );

  const handleScroll = React.useCallback((e: React.UIEvent<HTMLDivElement>) => {
    setScrollTop(e.currentTarget.scrollTop);
  }, []);

  const totalHeight = items.length * itemHeight;
  const offsetY = startIndex * itemHeight;

  return (
    <div
      className={`overflow-auto ${className}`}
      style={{ height: containerHeight }}
      onScroll={handleScroll}
    >
      <div style={{ height: totalHeight, position: 'relative' }}>
        <div style={{ transform: `translateY(${offsetY}px)` }}>
          {visibleItems.map((item, index) => (
            <div key={startIndex + index} style={{ height: itemHeight }}>
              {renderItem(item, startIndex + index)}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

/**
 * Optimized table component with row virtualization
 */
interface OptimizedTableProps<T> {
  data: T[];
  columns: Array<{
    key: keyof T;
    header: string;
    render?: (value: T[keyof T], item: T) => React.ReactNode;
    width?: string;
  }>;
  rowHeight?: number;
  maxHeight?: number;
  className?: string;
}

export function OptimizedTable<T extends Record<string, any>>({
  data,
  columns,
  rowHeight = 50,
  maxHeight = 400,
  className = ""
}: OptimizedTableProps<T>) {
  const renderRow = React.useCallback((item: T, index: number) => (
    <div 
      key={index} 
      className="flex border-b border-border hover:bg-accent/50"
      style={{ height: rowHeight }}
    >
      {columns.map((column) => (
        <div
          key={String(column.key)}
          className="flex items-center px-4 overflow-hidden"
          style={{ width: column.width || 'auto', flex: column.width ? 'none' : 1 }}
        >
          {column.render ? column.render(item[column.key], item) : String(item[column.key])}
        </div>
      ))}
    </div>
  ), [columns, rowHeight]);

  return (
    <div className={`border border-border rounded-lg ${className}`}>
      {/* Header */}
      <div className="flex bg-muted/50 border-b border-border">
        {columns.map((column) => (
          <div
            key={String(column.key)}
            className="flex items-center px-4 py-3 font-medium"
            style={{ width: column.width || 'auto', flex: column.width ? 'none' : 1 }}
          >
            {column.header}
          </div>
        ))}
      </div>
      
      {/* Virtual scrolling body */}
      <VirtualScroll
        items={data}
        itemHeight={rowHeight}
        containerHeight={maxHeight}
        renderItem={renderRow}
      />
    </div>
  );
}

/**
 * Debounced input component for search functionality
 */
interface DebouncedInputProps {
  value: string;
  onChange: (value: string) => void;
  delay?: number;
  placeholder?: string;
  className?: string;
}

export const DebouncedInput = memo<DebouncedInputProps>(({
  value,
  onChange,
  delay = 300,
  placeholder,
  className
}) => {
  const [localValue, setLocalValue] = React.useState(value);
  const timeoutRef = React.useRef<NodeJS.Timeout>();

  React.useEffect(() => {
    setLocalValue(value);
  }, [value]);

  const handleChange = React.useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = e.target.value;
    setLocalValue(newValue);

    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }

    timeoutRef.current = setTimeout(() => {
      onChange(newValue);
    }, delay);
  }, [onChange, delay]);

  React.useEffect(() => {
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, []);

  return (
    <input
      type="text"
      value={localValue}
      onChange={handleChange}
      placeholder={placeholder}
      className={className}
    />
  );
});

DebouncedInput.displayName = 'DebouncedInput';

/**
 * Image component with lazy loading and error handling
 */
interface OptimizedImageProps {
  src: string;
  alt: string;
  className?: string;
  fallbackSrc?: string;
  loading?: 'lazy' | 'eager';
}

export const OptimizedImage = memo<OptimizedImageProps>(({
  src,
  alt,
  className,
  fallbackSrc,
  loading = 'lazy'
}) => {
  const [imgSrc, setImgSrc] = React.useState(src);
  const [isLoading, setIsLoading] = React.useState(true);
  const [hasError, setHasError] = React.useState(false);

  const handleLoad = React.useCallback(() => {
    setIsLoading(false);
    setHasError(false);
  }, []);

  const handleError = React.useCallback(() => {
    setIsLoading(false);
    setHasError(true);
    if (fallbackSrc && imgSrc !== fallbackSrc) {
      setImgSrc(fallbackSrc);
    }
  }, [fallbackSrc, imgSrc]);

  React.useEffect(() => {
    setImgSrc(src);
    setIsLoading(true);
    setHasError(false);
  }, [src]);

  if (isLoading) {
    return <Skeleton className={className} />;
  }

  if (hasError && !fallbackSrc) {
    return (
      <div className={`flex items-center justify-center bg-muted ${className}`}>
        <span className="text-muted-foreground text-sm">Failed to load image</span>
      </div>
    );
  }

  return (
    <img
      src={imgSrc}
      alt={alt}
      className={className}
      loading={loading}
      onLoad={handleLoad}
      onError={handleError}
    />
  );
});

OptimizedImage.displayName = 'OptimizedImage';