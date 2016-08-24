# -*- coding: utf-8 -*-
import logging
import click
from datetime import datetime
import sys

from vcftoolbox import get_vcf_handle

from loqusdb.utils import get_family
from loqusdb.exceptions import CaseError
from loqusdb.utils import delete_variants
from . import base_command

logger = logging.getLogger(__name__)

@base_command.command()
@click.argument('variant_file',
                    type=click.Path(exists=True),
                    metavar='<vcf_file>'
)
@click.option('-f', '--family_file',
                    type=click.Path(exists=True),
                    metavar='<ped_file>'
)
@click.option('-t' ,'--family_type', 
                type=click.Choice(['ped', 'alt', 'cmms', 'mip']), 
                default='ped',
                help='If the analysis use one of the known setups, please specify which one.'
)
@click.option('-i', '--family_id',
                    type=str,
                    help='The id for the case to add'
)
@click.pass_context
def delete(ctx, variant_file, family_file, family_type, family_id):
    """Delete the variants of a case."""
    if not family_file or family_id:
        logger.error("Please provide a family file or a case id")
        logger.info("Exiting")
        ctx.abort()
    
    adapter = ctx.obj['adapter']

    start_deleting = datetime.now()
    try:
        delete = delete_variants(adapter, variant_stream, family_id,
                                affected_individuals)
    except CaseError as error:
        logger.warning(error.message)
        ctx.abort()

    logger.info("Nr of variants deleted: {0}".format(count))
    logger.info("Time to delete variants: {0}"
                .format(datetime.now() - start_deleting))
