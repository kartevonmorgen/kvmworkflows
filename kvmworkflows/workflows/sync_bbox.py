import asyncio

from datetime import timedelta
from temporalio import workflow


with workflow.unsafe.imports_passed_through():
    import numpy as np
    
    from loguru import logger
    
    from kvmworkflows.config.config import config
    from kvmworkflows.activities.get_tags import get_tags
    from kvmworkflows.activities.insert_tags import insert_tags
    from kvmworkflows.activities.get_search_entries import get_search
    from kvmworkflows.activities.insert_search_entries import upsert_search_entries
    

@workflow.defn
class Workflow:

    @workflow.run
    async def run(self):
        logger.info("Starting workflow")
        logger.info("Fetching tags")
        tags = await workflow.execute_activity(
            get_tags,
            start_to_close_timeout=timedelta(seconds=300),
        )
        logger.success(f"Tags fetched: {len(tags)}")
        
        logger.info("Inserting tags")
        await workflow.execute_activity(
            insert_tags,
            tags,
            start_to_close_timeout=timedelta(seconds=300),
        )
        logger.success("Tags inserted")

        tasks = []
        for area in config.areas:
            logger.info(f"Fetching entries for area: {area.name}")
            lats = np.linspace(area.lats[0], area.lats[1], num=area.lat_n_chunks)
            lngs = np.linspace(area.lngs[0], area.lngs[1], num=area.lng_n_chunks)
            for i in range(area.lat_n_chunks-1):
                for j in range(area.lng_n_chunks-1):
                    bbox = f"{lats[i]},{lngs[j]},{lats[i+1]},{lngs[j+1]}"

                    task = self.sync_search_bbox(bbox)
                    tasks.append(task)
        
        await asyncio.gather(*tasks)
        logger.success("Updating entries completed")
    
    async def sync_search_bbox(self, bbox: str):
        search_entries = await workflow.execute_activity(
            get_search,
            bbox,
            start_to_close_timeout=timedelta(seconds=300),
        )

        await workflow.execute_activity(
            upsert_search_entries,
            search_entries,
            start_to_close_timeout=timedelta(seconds=300),
        )
