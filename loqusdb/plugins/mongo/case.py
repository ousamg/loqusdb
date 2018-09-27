import logging
from pprint import pprint as pp

from loqusdb.plugins import BaseCaseMixin
from loqusdb.exceptions import CaseError

LOG = logging.getLogger(__name__)

class CaseMixin(BaseCaseMixin):

    def case(self, case):
        """Get a case from the database

            Search the cases with the case id

            Args:
                case (dict): A case dictionary

            Returns:
                mongo_case (dict): A mongo case dictionary
        """
        LOG.debug("Getting case {0} from database".format(case.get('case_id')))
        case_id = case['case_id']
        return self.db.case.find_one({'case_id': case_id})

    def cases(self):
        """Get all cases from the database

            Returns:
                cases (Iterable(Case)): A iterable with mongo cases
        """
        LOG.debug("Collecting all cases from database")
        return self.db.case.find()

    def add_case(self, case, update=False):
        """Add a case to the case collection

        If the case exists and update is False raise error.

        Args:
            db (MongoClient): A connection to the mongodb
            case (dict): A case dictionary
            update(bool): If existing case should be updated

        Returns:
            mongo_case_id(ObjectId)

        """
        existing_case = self.case(case)
        if existing_case and not update:
            raise CaseError("Case {} already exists".format(case['case_id']))
        mongo_case_id = self.db.case.replace_one(
            {
                'case_id': case['case_id'],
            },
            case,
            True
            ).upserted_id

        return mongo_case_id

    def delete_case(self, case):
        """Delete case from the database

            Delete a case from the database

            Args:
                case (dict): A case dictionary

        """
        mongo_case = self.case(case)

        if not mongo_case:
            raise CaseError("Tried to delete case {0} but could not find case".format(
                case.get('case_id')
            ))
        LOG.info("Removing case {0} from database".format(
            mongo_case.get('case_id')
        ))
        self.db.case.delete_one({'_id': mongo_case['_id']})

        return

    def case_count(self):
        """Returns the total number of cases in the database

        returns:
            nr_of_cases (int): Total number of cases in database
        """
        nr_of_cases = 0
        res = self.cases

        return res.count()
