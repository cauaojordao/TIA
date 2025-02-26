using Microsoft.EntityFrameworkCore;
using TIA.Domain.Entities;
using TIA.Domain.Interfaces;
using TIA.Persistence.Context;

namespace TIA.Persistence.Repositories
{
    public class UserRepository : BaseRepository<Account>, IUserRepository
    {
        public UserRepository(AppDbContext context) : base(context)
        { }

        public async Task<Account> GetByEmail(string email, CancellationToken cancellationToken)
        {
            return await Context.Users.FirstOrDefaultAsync(x => x.UserEmail == email, cancellationToken);
        }
    }
}
