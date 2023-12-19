from fastapi import HTTPException

from fairy_chess.database.tournment import TournmentModel, tournment_repository


class TournmentController:
    def create(name: str, starts_at: float, puuid: str):
        tournment_base = tournment_repository.find_by_name(name)
        if not tournment_base:
            tournment = TournmentModel(name=name, starts_at=starts_at, creator_id=puuid)
            tournment_repository.save(tournment)
            return tournment.model_dump()
        raise HTTPException(status_code=403, detail="Tournemt alredy exists")

    def fetch() -> list[dict]:
        return [tournment.model_dump() for tournment in tournment_repository.fetch()]

    def register(tournment_id: str, puuid: str):
        tournment_base = tournment_repository.find_one_by_id(tournment_id)
        if tournment_base and puuid not in tournment_base.competitors:
            tournment_base.competitors.append(puuid)
            tournment_repository.save(tournment_base)
            return tournment_base
        raise HTTPException(status_code=403, detail="User alredy register in this tournment")