import { ref, computed, type Ref } from 'vue';

// ============================================================
// PAGINATION UTILITAIRE
// ============================================================

export function usePagination<T>(items: Ref<T[]>, itemsPerPage: number = 5) {
  const currentPage = ref(1);

  const totalPages = computed(() => {
    return Math.ceil(items.value.length / itemsPerPage) || 1;
  });

  const paginatedItems = computed(() => {
    const start = (currentPage.value - 1) * itemsPerPage;
    const end = start + itemsPerPage;
    return items.value.slice(start, end);
  });

  const goToPage = (page: number) => {
    if (page >= 1 && page <= totalPages.value) {
      currentPage.value = page;
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  const nextPage = () => {
    if (currentPage.value < totalPages.value) {
      currentPage.value++;
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  const prevPage = () => {
    if (currentPage.value > 1) {
      currentPage.value--;
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  return {
    currentPage,
    totalPages,
    paginatedItems,
    goToPage,
    nextPage,
    prevPage
  };
}

// ============================================================
// POPUP UTILITAIRE
// ============================================================

export function usePopup() {
  const isOpen = ref(false);

  const openPopup = () => {
    isOpen.value = true;
  };

  const closePopup = () => {
    isOpen.value = false;
  };

  const togglePopup = () => {
    isOpen.value = !isOpen.value;
  };

  return {
    isOpen,
    openPopup,
    closePopup,
    togglePopup
  };
}
