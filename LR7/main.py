from src.src import AssociativeProcessor


if __name__ == '__main__':
    associative_processor = AssociativeProcessor(3, 4)
    print(associative_processor)
    print(f'Search in range result: {associative_processor.search_within_given_range("001", "100")}')
