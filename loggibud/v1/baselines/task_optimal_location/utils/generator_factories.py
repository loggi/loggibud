import os
import os.path
from loggibud.v1.types import CVRPInstance, JSONDataclassMixin, Point
from typing import List, Generator


def instancesGeneratorFactory(paths: List[str]):
  """This high order function takes directories list that contains CRVPInstance json files 
  inside each directory and returns a factory to access its Generator.
  It allows using Generator objects with the same context more than once.

  Expected param exemple (paths):

    ── dir0 -> (path param 0)

       ├── CRVPFile_exemple0.json

       └──...

    ── dir1 -> (path param 1)

       ├── CRVPFile_exemple1.json

       └──...

  Typical usage example:

      instanceFactory = instancesGeneratorFactory(paths)

      instances = instanceFactory()

  Args:
      paths (List[str]): List of directories 

  Returns:
      instanceGenerator() -> Generator[JSONDataclassMixin]
  """  
  def instancesGenerator() -> Generator[JSONDataclassMixin]:
    """Generator[JSONDataclassMixin] Factory with path context given before at 
    instancesGeneratorFactory(paths)

    Returns:
        Generator[JSONDataclassMixin]
    Yields:
        JSONDataclassMixin
    """    
    return (
      CVRPInstance.from_file(os.path.join(path, json_file))
      for path in paths
      for json_file in os.listdir(path) if json_file.endswith('.json')
    )

  return instancesGenerator


def pointsClientsGeneratorFactory(instancesFactory):
  """This high order function receives a instanceGenerator,
  and returns a Generator of clients (In that case, a client must be
  all points for every delivery of the instances generator given)

  Typical usage example:

  instanceFactory = instancesGeneratorFactory(paths)

  pointsClientsFactory = pointsClientsGeneratorFactory(instanceFactory)

  clients = pointsClientsFactory()

  Args:
      instanceGenerator():
  """  
  def pointsClients() -> Generator[Point]:
    """Clients Factory with instancesGenerator context given

    Returns:
        Generator[Point]

    Yields:
        Point
    """    
    return (
      d.point
      for instance in instancesFactory()
      for d in instance.deliveries
    )

  return pointsClients