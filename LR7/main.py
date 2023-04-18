from src.src import AssociativeProcessor


if __name__ == '__main__':
    associative_processor = AssociativeProcessor(3, 10)
    print(associative_processor)
    print(f'Search in range result: {associative_processor.search_within_given_range("001", "100")}')
    print(f'Pattern search: {associative_processor.closest_pattern_search("00x")}')
