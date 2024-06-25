from ising import (intialize_system,
                   random_site,
                   neighbour_states,
                   like_neighbours,
                   energy_difference,
                   successful_swap)


def test_intialize_system():

    assert len(intialize_system(0,0)) == 0, "should be 0"
    
    assert len(intialize_system(1,0)) == 0, "should be 0"
    assert len(intialize_system(0,1)) == 0, "should be 0"
    assert len(intialize_system(1,1)) == 1, "should be 1"
    assert len(intialize_system(1,1)[0]) == 1, "should be 1"

    assert len(intialize_system(3,0)) == 0, "should be 0"
    assert len(intialize_system(0,3)) == 0, "should be 0"
    assert len(intialize_system(3,3)) == 3, "should be 3"
    assert len(intialize_system(3,3)[0]) == 3, "should be 3"


def test_random_site():

    assert random_site(1,1) == (0,0), "should be (0,0)"
    assert len(random_site(2,2)) == 2


def test_neighbour_states():

    assert neighbour_states([[0,1],[0,0]], (0,0)) == [1,0,0], "should be [1,0,0]"
    assert neighbour_states([[0,1],[0,0]], (1,0)) == [0,0,0], "should be [0,0,0]"
    assert neighbour_states([[0,1],[0,0]], (0,1)) == [0,1,0], "should be [0,1,0]"
    assert neighbour_states([[0,1],[0,0]], (1,1)) == [0,1,0], "should be [0,1,0]"

    assert neighbour_states([[1,0,0],[0,1,0],[1,1,1]], (0,0)) == [0,0,1], "should be [0,0,1]"
    assert neighbour_states([[1,0,0],[0,1,0],[1,1,1]], (1,0)) == [1,0,0,1,0], "should be [1,0,0,1,0]"
    assert neighbour_states([[1,0,0],[0,1,0],[1,1,1]], (2,0)) == [0,1,0], "should be [0,1,0]"
    assert neighbour_states([[1,0,0],[0,1,0],[1,1,1]], (0,1)) == [1,0,1,1,1], "should be [1,0,1,1,1]"
    assert neighbour_states([[1,0,0],[0,1,0],[1,1,1]], (1,1)) == [1,0,0,0,0,1,1,1], "should be [1,0,0,0,0,1,1,1]"
    assert neighbour_states([[1,0,0],[0,1,0],[1,1,1]], (2,1)) == [0,0,1,1,1], "should be [0,0,1,1,1]"
    assert neighbour_states([[1,0,0],[0,1,0],[1,1,1]], (0,2)) == [0,1,1], "should be [0,1,1]"
    assert neighbour_states([[1,0,0],[0,1,0],[1,1,1]], (1,2)) == [0,1,0,1,1], "should be [0,1,0,1,1]"
    assert neighbour_states([[1,0,0],[0,1,0],[1,1,1]], (2,2)) == [1,0,1], "should be [1,0,1]"


def test_like_neighbours():

    assert like_neighbours([[0,1],[0,0]], (0,0), 0) == 2, "should be 1"
    assert like_neighbours([[0,1],[0,0]], (0,0), 1) == 1, "should be 2"
    assert like_neighbours([[0,1],[0,0]], (1,0), 0) == 3, "should be 3"
    assert like_neighbours([[0,1],[0,0]], (1,0), 1) == 0, "should be 0"


def test_energy_difference():

    assert energy_difference([[0,1],[0,0]], (0,0)) == 1, "should be [1,0,0]"
    assert energy_difference([[0,1],[0,0]], (1,0)) == -3, "should be [0,0,0]"
    assert energy_difference([[0,1],[0,0]], (0,1)) == 1, "should be [0,1,0]"
    assert energy_difference([[0,1],[0,0]], (1,1)) == 1, "should be [0,1,0]"


def test_successful_swap():

    assert successful_swap(0, 0) == True
    assert successful_swap(1, 0) == False
    assert successful_swap(-1, 0) == True
    assert successful_swap(1e6, 0) == False
    assert successful_swap(-1e6, 0) == True


if __name__ == "__main__":
    test_intialize_system()
    test_random_site()
    test_neighbour_states()
    test_like_neighbours()
    test_energy_difference()
    test_successful_swap()
    print("Everything passed")